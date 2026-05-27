"""
This script demonstrates a headless computational stack suitable for quantum hardware engineering
and Electronic Design Automation (EDA) workflows using Quantum Metal, PHIDL, GDSTK, and CuPy.

Authored by Onri Jay Benally (2026)

Open Access (CC-BY-4.0)
"""

import os
import sys
import subprocess
import shutil
import textwrap
import re
import importlib
from pathlib import Path
from typing import Final

# =============================================================================
# CONTROL KNOBS
# =============================================================================
# The INSTALL_EXTRAS tuple configures the modular packages to append during deployment.
# Available composable options include:
#   'headless' : Restricts Graphical User Interface components for remote stability.
#   'gui'      : Installs PySide2 and pyvista for graphical interaction.
#   'mesh'     : Installs gmsh for finite element mesh generation.
#   'gmesh'    : Alternative alias mapping to the mesh generation tools.
#   'ansys'    : Installs dependencies for Ansys interoperability.
#   'full'     : Installs all available extra packages simultaneously.
INSTALL_EXTRAS: Final[tuple[str, ...]] = ("headless", "mesh")

RESTART_AFTER_INSTALL: Final[bool] = True
QT_QPA_PLATFORM: Final[str] = "offscreen"
MPLBACKEND: Final[str] = "module://matplotlib_inline.backend_inline"
USE_CUPY_WHEN_AVAILABLE: Final[bool] = True

# Publication visualization parameters
MPL_DPI: Final[int] = 250
MPL_FONT_SANS_SERIF: Final[list[str]] = ['Tahoma', 'DejaVu Sans']
MPL_FONT_WEIGHT: Final[str] = 'normal'

QISKIT_METAL_REPO_URL: Final[str] = "https://github.com/qiskit-community/qiskit-metal"
QISKIT_METAL_BRANCH: Final[str] = "v0.7.1"
QISKIT_METAL_ROOT: Final[Path] = Path("/content/qiskit-metal")

BINARY_FOUNDATION_PACKAGES: Final[list[str]] = [
    "numpy==1.26.4",
    "pandas==2.2.2",
    "scipy==1.14.1",
    "matplotlib==3.8.4",
    "h5py==3.11.0",
]

EDA_PACKAGES: Final[list[str]] = [
    "gdstk>=0.9.61,<1.0.0",
    "shapely>=2.0.0,<3.0.0",
    "ezdxf>=1.2.0,<2.0.0",
    "phidl>=1.7.2,<2.0.0",
    "networkx>=2.8",
    "pint>=0.20",
    "addict>=2.4.0",
    "pyyaml>=6.0.1",
    "descartes>=1.1",
    "jedi>=0.19.1",
]

GPU_PACKAGES: Final[list[str]] = [
    "cupy-cuda12x>=13.0.0,<14.0.0",
]

os.environ["QT_QPA_PLATFORM"] = QT_QPA_PLATFORM


def configure_visualization() -> None:
    """Apply default rendering configurations for inline plot generation."""
    try:
        from matplotlib import rcParams
        rcParams['figure.dpi'] = MPL_DPI
        rcParams['font.sans-serif'] = MPL_FONT_SANS_SERIF
        rcParams['font.weight'] = MPL_FONT_WEIGHT
    except ImportError:
        pass


def run_command(command: list[str], cwd: Path | None = None) -> None:
    """Execute a synchronous subprocess command and raise an exception upon failure."""
    print(f"Executing {' '.join(command)}")
    subprocess.check_call(command, cwd=str(cwd) if cwd else None)


def install_stack() -> None:
    """Install a coherent compiled package stack utilizing the accelerated resolver."""
    # Bootstrap the accelerated resolver using the native package manager.
    run_command([
        sys.executable, "-m", "pip", "install", "-q", "--upgrade", 
        "uv", "pip", "wheel", "setuptools"
    ])

    # Deploy the foundational binaries via the accelerated resolver.
    run_command([
        sys.executable, "-m", "uv", "pip", "install", "--system", "-q", "--upgrade",
        "--reinstall", "--no-cache", 
        *BINARY_FOUNDATION_PACKAGES
    ])

    # Deploy the engineering and hardware acceleration libraries concurrently.
    run_command([
        sys.executable, "-m", "uv", "pip", "install", "--system", "-q", "--upgrade",
        "--no-cache", 
        *EDA_PACKAGES, *GPU_PACKAGES
    ])


def clone_qiskit_metal() -> None:
    """Clone the specified version of the Quantum Metal repository into the workspace."""
    if QISKIT_METAL_ROOT.exists():
        shutil.rmtree(QISKIT_METAL_ROOT)
    
    run_command([
        "git",
        "clone",
        "--depth",
        "1",
        "--branch",
        QISKIT_METAL_BRANCH,
        QISKIT_METAL_REPO_URL,
        str(QISKIT_METAL_ROOT),
    ])


def find_qiskit_metal_package() -> tuple[Path, Path]:
    """Locate and return the import root alongside the main package directory."""
    candidates = [
        QISKIT_METAL_ROOT / "qiskit_metal",
        QISKIT_METAL_ROOT / "src" / "qiskit_metal",
    ]
    for package_dir in candidates:
        if package_dir.exists():
            return package_dir.parent, package_dir

    raise FileNotFoundError(
        f"Could not locate the package root under {QISKIT_METAL_ROOT}. "
        f"Searched directories included {candidates}"
    )


def backup_file(path: Path) -> None:
    """Create a one-time backup of a target file prior to applying headless patches."""
    backup_path = path.with_name(f"{path.stem}__orig{path.suffix}")
    if path.exists() and not backup_path.exists():
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def write_minimal_qiskit_metal_init(package_dir: Path) -> None:
    """Replace the primary initialization file with a headless surface."""
    init_path = package_dir / "__init__.py"
    backup_file(init_path)
    minimal_init = textwrap.dedent(
        """
        # Headless initialization surface for Google Colaboratory.
        import logging as _logging
        try:
            from addict import Dict as Dict
        except Exception:
            from .toolbox_python.attr_dict import Dict

        logger = _logging.getLogger("qiskit_metal_colab")

        class _Config:
            @staticmethod
            def is_building_docs():
                return False

        config = _Config()

        def is_design(obj):
            try:
                from .designs.design_base import QDesign
                return isinstance(obj, QDesign)
            except Exception:
                return False

        def is_component(obj):
            try:
                from .qlibrary.core.base import QComponent
                return isinstance(obj, QComponent)
            except Exception:
                return False

        __all__ = ["Dict", "config", "logger", "is_design", "is_component"]
        """
    ).strip() + "\n"
    init_path.write_text(minimal_init, encoding="utf-8")


def patch_draw_package(package_dir: Path) -> None:
    """Isolate drawing module imports to ensure GUI libraries remain unloaded."""
    draw_init = package_dir / "draw" / "__init__.py"
    if not draw_init.exists():
        return
    backup_file(draw_init)
    text = draw_init.read_text(encoding="utf-8")
    
    text = re.sub(
        r"^\s*from\s+\.\s*import\s+mpl\s*$",
        "try:\n"
        "    from . import mpl\n"
        "except Exception as _draw_mpl_error:\n"
        "    print('[colab] draw.mpl disabled in headless mode', _draw_mpl_error)\n",
        text,
        flags=re.MULTILINE,
    )
    
    text = re.sub(
        r"^\s*from\s+\.mpl\s+import[^\n]*$",
        "try:\n"
        "    from .mpl import render, figure_spawn\n"
        "except Exception as _draw_named_error:\n"
        "    print('[colab] draw.mpl named imports disabled', _draw_named_error)\n"
        "    def render(*args, **kwargs):\n"
        "        raise RuntimeError('draw.mpl unavailable in headless mode')\n"
        "    def figure_spawn(*args, **kwargs):\n"
        "        raise RuntimeError('draw.mpl unavailable in headless mode')\n",
        text,
        flags=re.MULTILINE,
    )
    draw_init.write_text(text, encoding="utf-8")


def patch_renderers_package(package_dir: Path) -> None:
    """Enforce explicit rendering imports to bypass automated initialization errors."""
    renderer_init = package_dir / "renderers" / "__init__.py"
    if not renderer_init.exists():
        return
    backup_file(renderer_init)
    renderer_init.write_text(
        "# Minimal renderers package targeting explicit imports only.\n"
        "__all__ = []\n",
        encoding="utf-8",
    )


def setup_qiskit_metal() -> Path:
    """Execute the full sequence to clone, patch, and link the repository."""
    clone_qiskit_metal()
    
    extras_formatted = ",".join(INSTALL_EXTRAS)
    package_target = f".[{extras_formatted}]" if extras_formatted else "."
    
    # Delegate the complex local repository installation to the accelerated resolver.
    run_command([
        sys.executable, "-m", "uv", "pip", "install", "--system", "-q", "-e", package_target
    ], cwd=QISKIT_METAL_ROOT)

    import_root, package_dir = find_qiskit_metal_package()
    
    if "headless" in INSTALL_EXTRAS:
        write_minimal_qiskit_metal_init(package_dir)
        patch_draw_package(package_dir)
        patch_renderers_package(package_dir)

    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = (
        str(import_root)
        if not existing_pythonpath
        else f"{import_root}:{existing_pythonpath}"
    )

    if "qiskit_metal" in sys.modules:
        del sys.modules["qiskit_metal"]
    importlib.invalidate_caches()

    import qiskit_metal

    imported_from = Path(qiskit_metal.__file__).resolve()
    expected_init = package_dir.resolve() / "__init__.py"
    
    if imported_from != expected_init:
        raise RuntimeError(
            f"Repository imported from incorrect location. "
            f"Found {imported_from} while anticipating {expected_init}."
        )

    print(f"Quantum Metal successfully imported from {imported_from}")
    return package_dir


if __name__ == "__main__":
    print("Initiating foundation installation via accelerated resolver.")
    install_stack()
    
    print("Initiating repository deployment.")
    QISKIT_METAL_PACKAGE_DIR = setup_qiskit_metal()
    
    configure_visualization()

    if RESTART_AFTER_INSTALL:
        print("Restarting the runtime environment gracefully to synchronize binaries.")
        import IPython
        IPython.Application.instance().kernel.do_shutdown(True)
    else:
        print("Installation complete. Please manually restart the runtime if necessary.")
