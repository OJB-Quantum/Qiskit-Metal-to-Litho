# openEMS Colab installer.
"""
Authored by Onri Jay Benally (2026)

Open Access (CC-BY-4.0)
"""

import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


# =============================================================================
# CONTROL KNOBS
# =============================================================================

INSTALL_APT_PACKAGES = True
PYTHON_BRIDGE_REQUIRED = False
OCTAVE_BRIDGE_REQUIRED = False
RUN_APT_UPDATE = True

LOG_DIR = Path("/content/openems_install_logs")
BRIDGE_MODULE_PATH = Path("/content/openems_colab_bridge.py")
SMOKE_TEST_DIR = Path("/content/openems_smoke_tests")

APT_PACKAGES = (
    "openems",
    "python3-openems",
    "libopenems-dev",
    "octave-openems",
    "octave",
    "python3-numpy",
    "python3-h5py",
    "python3-matplotlib",
    "python3-scipy",
)

PYTHON_CANDIDATES = (
    "/usr/bin/python3",
    "/usr/bin/python3.10",
    "/usr/bin/python3.11",
)


# =============================================================================
# COMMAND HELPERS
# =============================================================================

def run_command(
    command: list[str],
    *,
    check: bool = True,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
    log_name: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command, print its tail, and optionally save a log."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    print("$ " + " ".join(command))

    result = subprocess.run(
        command,
        check=False,
        cwd=str(cwd) if cwd is not None else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    output = result.stdout or ""
    if log_name is not None:
        path = LOG_DIR / log_name
        path.write_text(output, encoding="utf-8", errors="replace")
        print(f"log written to {path}")

    if output:
        print(output[-5000:])

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed with code {result.returncode}: "
            + " ".join(command)
        )

    return result


def command_exists(command_name: str) -> bool:
    """Return True when a command exists on PATH."""
    return shutil.which(command_name) is not None


def apt_candidate_exists(package_name: str) -> bool:
    """Return True when apt can install a package."""
    if not command_exists("apt-cache"):
        return False

    result = run_command(
        ["apt-cache", "policy", package_name],
        check=False,
        log_name=f"apt_policy_{package_name}.log",
    )
    text = result.stdout or ""
    return "Candidate:" in text and "Candidate: (none)" not in text


def apt_install_available(packages: tuple[str, ...]) -> None:
    """Install packages available from the current Colab apt repositories."""
    if RUN_APT_UPDATE:
        run_command(
            ["apt-get", "update", "-qq"],
            check=False,
            log_name="apt_update.log",
        )

    available = tuple(pkg for pkg in packages if apt_candidate_exists(pkg))
    skipped = tuple(pkg for pkg in packages if pkg not in available)

    if skipped:
        print("Skipped unavailable apt packages:")
        for package_name in skipped:
            print(f"  {package_name}")

    if not available:
        raise RuntimeError("No requested apt packages were available.")

    run_command(
        ["apt-get", "install", "-y", "-qq", *available],
        check=True,
        log_name="apt_install_openems.log",
    )


# =============================================================================
# ENVIRONMENTS AND DIAGNOSTICS
# =============================================================================

def clean_system_env() -> dict[str, str]:
    """Return a minimal environment for apt-provided Python bindings."""
    return {
        "HOME": os.environ.get("HOME", "/root"),
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONNOUSERSITE": "1",
        "PYTHONPATH": "/usr/lib/python3/dist-packages",
    }


def openems_binaries_available() -> bool:
    """Return True when command-line openEMS executables are available."""
    ok = True
    for name in ("openEMS", "AppCSXCAD"):
        path = shutil.which(name)
        if path is None:
            print(f"Missing executable: {name}")
            ok = False
        else:
            print(f"Found executable: {name} -> {path}")
    return ok


def print_package_locations() -> None:
    """Print installed openEMS package locations for debugging."""
    for package_name in ("python3-openems", "openems", "octave-openems"):
        result = run_command(
            ["dpkg", "-L", package_name],
            check=False,
            env=clean_system_env(),
            log_name=f"dpkg_L_{package_name}.log",
        )
        if result.returncode == 0:
            interesting = [
                line
                for line in (result.stdout or "").splitlines()
                if (
                    "dist-packages" in line
                    or "/usr/share/openEMS" in line
                    or "/usr/share/CSXCAD" in line
                )
            ]
            print(f"Key files from {package_name}:")
            for line in interesting[:80]:
                print("  " + line)


# =============================================================================
# PYTHON AND OCTAVE PROBES
# =============================================================================

def python_probe_code() -> str:
    """Return the Python probe used to verify openEMS bindings."""
    return r'''
import importlib.util
import sys

print("python executable:", sys.executable)
print("python version:", sys.version.replace("\\n", " "))
print("sys.path:")
for item in sys.path:
    print("  " + str(item))

for module_name in ("CSXCAD", "openEMS"):
    spec = importlib.util.find_spec(module_name)
    print(f"spec {module_name}: {spec}")
    if spec is not None:
        print(f"origin {module_name}: {spec.origin}")
        print(f"locations {module_name}: {spec.submodule_search_locations}")

from CSXCAD import ContinuousStructure
from openEMS import openEMS

csx = ContinuousStructure()
fdtd = openEMS()

print("ContinuousStructure:", type(csx))
print("openEMS:", type(fdtd))
print("OPENEMS_PYTHON_BINDINGS_OK")
'''


def test_python_candidate(python_executable: str) -> bool:
    """Return True when one Python executable can import openEMS bindings."""
    if not Path(python_executable).exists():
        return False

    safe_name = Path(python_executable).name.replace(".", "_")
    result = run_command(
        [python_executable, "-c", python_probe_code()],
        check=False,
        env=clean_system_env(),
        log_name=f"probe_openems_{safe_name}.log",
    )
    return (
        result.returncode == 0
        and "OPENEMS_PYTHON_BINDINGS_OK" in (result.stdout or "")
    )


def select_openems_python() -> str | None:
    """Return a Python executable that can import openEMS, if one exists."""
    candidates = []
    candidates.extend(PYTHON_CANDIDATES)
    candidates.append(sys.executable)

    seen: set[str] = set()
    for candidate in candidates:
        path = shutil.which(candidate) if "/" not in candidate else candidate
        if path is None or path in seen:
            continue
        seen.add(path)
        print(f"Testing openEMS Python candidate: {path}")
        if test_python_candidate(path):
            print(f"Selected openEMS Python executable: {path}")
            return path

    return None


def octave_probe_code() -> str:
    """Return an Octave probe for the openEMS interface."""
    return """
addpath('/usr/share/openEMS/matlab');
addpath('/usr/share/CSXCAD/matlab');
disp('Octave path configured for openEMS');
which openEMS
which InitFDTD
which WriteOpenEMS
disp('OPENEMS_OCTAVE_INTERFACE_OK');
"""


def test_octave_interface() -> bool:
    """Return True when the Octave openEMS interface is available."""
    if not shutil.which("octave"):
        print("Octave executable is unavailable.")
        return False

    SMOKE_TEST_DIR.mkdir(parents=True, exist_ok=True)
    script_path = SMOKE_TEST_DIR / "openems_octave_probe.m"
    script_path.write_text(octave_probe_code(), encoding="utf-8")

    result = run_command(
        ["octave", "--quiet", str(script_path)],
        check=False,
        env=clean_system_env(),
        log_name="probe_openems_octave.log",
    )
    return (
        result.returncode == 0
        and "OPENEMS_OCTAVE_INTERFACE_OK" in (result.stdout or "")
    )


# =============================================================================
# BRIDGE MODULE WRITER
# =============================================================================

def write_bridge_module(
    python_executable: str | None,
    octave_available: bool,
) -> None:
    """Write a Colab bridge module without nested-string syntax hazards."""
    python_literal = repr(python_executable) if python_executable else "None"
    octave_literal = "True" if octave_available else "False"

    bridge_code = f'''
from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path
from typing import Mapping


OPENEMS_PYTHON = {python_literal}
OCTAVE_AVAILABLE = {octave_literal}
DEFAULT_WORK_DIR = Path("/content/openems_runs")


def _base_env(extra_env: Mapping[str, str] | None = None) -> dict[str, str]:
    env = {{
        "HOME": os.environ.get("HOME", "/root"),
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONNOUSERSITE": "1",
        "PYTHONPATH": "/usr/lib/python3/dist-packages",
    }}
    if extra_env:
        env.update({{str(key): str(value) for key, value in extra_env.items()}})
    return env


def run_openems_binary(
    xml_path: str | Path,
    *,
    work_dir: str | Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    path = Path(xml_path)
    cwd = Path(work_dir) if work_dir is not None else path.parent
    result = subprocess.run(
        ["/usr/bin/openEMS", str(path)],
        cwd=str(cwd),
        env=_base_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args,
            output=result.stdout,
        )
    return result


def run_openems_python_script(
    script_path: str | Path,
    *,
    work_dir: str | Path | None = None,
    extra_env: Mapping[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    if OPENEMS_PYTHON is None:
        raise RuntimeError(
            "No compatible openEMS Python binding was found. "
            "Use run_openems_octave_code() or run_openems_binary()."
        )

    path = Path(script_path)
    cwd = Path(work_dir) if work_dir is not None else path.parent
    cwd.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [OPENEMS_PYTHON, str(path)],
        cwd=str(cwd),
        env=_base_env(extra_env),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args,
            output=result.stdout,
        )
    return result


def run_openems_python_code(
    code: str,
    *,
    work_dir: str | Path = DEFAULT_WORK_DIR,
    filename: str = "openems_case.py",
    extra_env: Mapping[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    cwd = Path(work_dir)
    cwd.mkdir(parents=True, exist_ok=True)
    script_path = cwd / filename
    script_path.write_text(
        textwrap.dedent(code).strip() + "\\n",
        encoding="utf-8",
    )
    return run_openems_python_script(
        script_path,
        work_dir=cwd,
        extra_env=extra_env,
        check=check,
    )


def run_openems_octave_code(
    code: str,
    *,
    work_dir: str | Path = DEFAULT_WORK_DIR,
    filename: str = "openems_case.m",
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    if not OCTAVE_AVAILABLE:
        raise RuntimeError("The Octave openEMS interface was unavailable.")

    cwd = Path(work_dir)
    cwd.mkdir(parents=True, exist_ok=True)
    script_path = cwd / filename
    prefix = """
addpath('/usr/share/openEMS/matlab');
addpath('/usr/share/CSXCAD/matlab');
"""
    script_path.write_text(
        textwrap.dedent(prefix + "\\n" + code).strip() + "\\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["/usr/bin/octave", "--quiet", str(script_path)],
        cwd=str(cwd),
        env=_base_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args,
            output=result.stdout,
        )
    return result
'''
    BRIDGE_MODULE_PATH.write_text(
        textwrap.dedent(bridge_code).strip() + "\n",
        encoding="utf-8",
    )
    print(f"Wrote bridge module: {BRIDGE_MODULE_PATH}")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    """Install openEMS and write a robust Colab bridge."""
    print("openEMS Colab installer")
    print(f"Notebook Python: {sys.executable}")
    print(f"Log directory:   {LOG_DIR}")

    if INSTALL_APT_PACKAGES:
        apt_install_available(APT_PACKAGES)

    binaries_ok = openems_binaries_available()
    if not binaries_ok:
        raise RuntimeError("openEMS command-line binaries were unavailable.")

    print_package_locations()

    openems_python = select_openems_python()
    octave_ok = test_octave_interface()

    if PYTHON_BRIDGE_REQUIRED and openems_python is None:
        raise RuntimeError(
            "A compatible Python binding was not found. "
            f"See logs in {LOG_DIR}."
        )

    if OCTAVE_BRIDGE_REQUIRED and not octave_ok:
        raise RuntimeError(
            "The Octave openEMS interface was not found. "
            f"See logs in {LOG_DIR}."
        )

    write_bridge_module(openems_python, octave_ok)

    print("\nInstallation summary")
    print(f"  openEMS binaries:      {binaries_ok}")
    print(f"  Python binding bridge: {openems_python}")
    print(f"  Octave bridge:         {octave_ok}")

    print("\nUse this in later Colab cells:")
    print(
        "import sys\n"
        "sys.path.insert(0, '/content')\n"
        "from openems_colab_bridge import (\n"
        "    run_openems_binary,\n"
        "    run_openems_octave_code,\n"
        "    run_openems_python_code,\n"
        ")\n"
    )

    if openems_python is not None:
        print(
            "run_openems_python_code(\"\"\"\n"
            "from CSXCAD import ContinuousStructure\n"
            "from openEMS import openEMS\n"
            "print('openEMS Python bridge works')\n"
            "\"\"\")\n"
        )
    elif octave_ok:
        print(
            "run_openems_octave_code(\"\"\"\n"
            "disp('openEMS Octave bridge works');\n"
            "which openEMS\n"
            "\"\"\")\n"
        )
    else:
        print(
            "# Python and Octave interfaces were unavailable, but the openEMS "
            "binary can still run XML files:\n"
            "# run_openems_binary('/content/path/to/simulation.xml')\n"
        )

main()
