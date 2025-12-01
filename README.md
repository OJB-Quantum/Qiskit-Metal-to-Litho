# Qiskit-Metal-to-Litho

[![License](https://img.shields.io/badge/Creative_Commons-License-green)](https://choosealicense.com/licenses/cc-by-4.0) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OJB-Quantum/Qiskit-Metal-to-Litho/main)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14621303.svg)](https://doi.org/10.5281/zenodo.14621303)

On the use of Qiskit Metal coded in Python to generate design files for building quantum devices on a chip, performed via direct-write lithography. Depending on the resolution of desired quantum device features, LASER, scanning thermal probe, and electron-beam techniques are applicable options for patterning your design. - Onri Jay Benally

(Note: in the patterned 400-transmon example below, the ground contacts were excluded from layout as the design was to demonstrate process feasibility from Qiskit Metal design-to-real-chip. However, the main features are clearly visible under optical microscopy. Also, I included a DXF/GDS design output for a [full quantum chip](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/blob/main/GDS%20Files/Full%20Chip%20Ex-001.GDS), ready for fabrication [electrodes, ground, and all], available to download in the file directories above).

![20230616_081944](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/7c20c740-19f3-4a0e-b471-a6ab591f89c0)

| It Is Important to Know That There Are 2 Main Types of Patterning With the E-Beam Writer (EBPG) Equipment: | Description |
| - | - |
| Marker-based using "rp" commands | This is used if your sample has pre-existing markers patterned on it already [ex. sample WITH purposely-designed reference points that can be automatically located by the EBPG's built-in SEM tool]. |
| Marker-free-based using "joyplus" commands | This is used if your sample has no pre-existing referencing patterns [ex. bare substrate or other sample WITHOUT purposely-designed reference points]. |

| Terms To Be Aware Of: | Description |
| - | - |
| BEAMER | Desktop software for importing GDSII or GDS files stored on WinSCP, beam step, size, and error correction (heal) paramters are set here and subsequently exported as GPF files that can be read by the EBPG equipment. Additionally the parameters can be downloaded as a Python script (.py). An example of a Python script used in BEAMER is available for reference in the file directory above. |
| CJOB | Software tool that is accessed on the EBPG equipment itself using the EBPG's terminal. From here, the GPF files can be uploaded and programmed with virtual alignment marker locations based on the uploaded design. Once the file is ready, it will export as a JOB file (.job). The JOB file name is what gets copied into the EBPG's terminal along with 4 coordinates validated by the built-in SEM. |
| Marker | The use of reference points on a coordinate plane that are assigned to a pre-existing, detectable pattern on a chip sample. Detection is performed automatically by the lithography equipment using commands such as "rp20". |
| Marker-free | The use of virtual reference points assigned to the region of interest to be patterned on a bare chip sample, wafer substrate, or other sample with without detectable markers. |

---

| If You Need to Install pip Through Python (Locally), Follow These Steps: |
| - |
| • First, install an EXE file of Python from: https://www.python.org/downloads |
| • Then, install pip by entering the following command into local terminal: 
```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py``` |
| • Now, pip is ready for use! |

| Local Installation Steps for Qiskit Metal: |
| - |
| [Installing Qiskit Metal Using Git+URL_by Onri Jay Benally](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/blob/main/Installing%20Qiskit%20Metal%20Using%20Git%2BURL_by%20Onri%20Jay%20Benally.pdf) |

### To Install and Run Qiskit Metal for Layout Generation Fully in Google Colab, Run These 2 Code Cells Up Front (By Onri)

(This will clone the official Qiskit Metal GitHub repository into Google Colab on any browser)

```
#@title Headless (Qt off) + dependencies
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["MPLBACKEND"] = "Agg"

import matplotlib as mpl
try:
    mpl.use("Agg", force=True)
except TypeError:
    mpl.use("Agg")
print("Matplotlib backend:", mpl.get_backend())

# Scientific + GDS toolchain (incl. Descartes)
!pip install "jedi>=0.16"
%pip -q install --upgrade pip wheel setuptools
%pip -q install "numpy>=1.24" "matplotlib>=3.8" \
                "gdstk>=0.9.61" "shapely>=2.0" "ezdxf>=1.2.0" \
                "pandas>=2.0" "scipy>=1.10" "networkx>=2.8" \
                "pint>=0.20" "addict>=2.4.0" "pyyaml>=6.0.1" \
                "qutip>=4.7" "h5py>=3.8" "descartes>=1.1" "jedi>=0.19.1"
```

```
#@title Clone Qiskit Metal; bind to /content/qiskit-metal; headless, layout-only init (Dict + is_component)
# pylint: disable=invalid-name
import os, sys, re, textwrap
from pathlib import Path

# Fresh clone
!rm -rf /content/qiskit-metal
!git clone --depth 1 https://github.com/qiskit-community/qiskit-metal /content/qiskit-metal

root = Path("/content/qiskit-metal")
pkg  = root / "qiskit_metal"
assert pkg.exists(), f"Package folder missing: {pkg}"

# Force Python to import FROM THIS FOLDER (no editable install)
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
os.environ["PYTHONPATH"] = str(root) + (":" + os.environ.get("PYTHONPATH",""))

# --- Replace qiskit_metal/__init__.py with a minimal but compatible headless init ---
orig_init = (pkg / "__init__.py").read_text(encoding="utf-8")
(pkg / "__init__orig.py").write_text(orig_init, encoding="utf-8")

minimal_init = textwrap.dedent("""
    # [colab] Headless, layout-only __init__ (no GUI, no analyses), keep essentials.
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
""").strip()+"\n"
(pkg / "__init__.py").write_text(minimal_init, encoding="utf-8")

# --- Scrub ALL draw.mpl imports to avoid PySide2 at import time ---
draw_init = pkg / "draw" / "__init__.py"
if draw_init.exists():
    d = draw_init.read_text(encoding="utf-8")
    # Guard "from . import mpl"
    d = re.sub(r'^\s*from\s+\.\s*import\s+mpl\s*$',
               "try:\n    from . import mpl\n"
               "except Exception as _e:\n"
               "    print('[colab] draw.mpl disabled (headless):', _e)\n",
               d, flags=re.MULTILINE)
    # Guard "from .mpl import ..." and any other .mpl imports
    d = re.sub(r'^\s*from\s+\.\s*mpl\s+import[^\n]*$',
               "try:\n    from .mpl import render, figure_spawn\n"
               "except Exception as _e:\n"
               "    print('[colab] draw.mpl (named) disabled (headless):', _e)\n"
               "    def render(*a, **k):\n"
               "        raise RuntimeError('draw.mpl unavailable in headless mode')\n"
               "    def figure_spawn(*a, **k):\n"
               "        raise RuntimeError('draw.mpl unavailable in headless mode')\n",
               d, flags=re.MULTILINE)
    draw_init.write_text(d, encoding="utf-8")

# Optional: ensure renderers package never drags Qt; keep explicit imports only
rndr_init = pkg / "renderers" / "__init__.py"
if rndr_init.exists():
    (rndr_init.parent / "__init__orig.py").write_text(rndr_init.read_text(encoding="utf-8"), encoding="utf-8")
    rndr_init.write_text("# [colab] minimal renderers package (explicit imports only; no Qt/MPL)\n__all__ = []\n",
                         encoding="utf-8")

# Verify: import the package *from this folder* and keep it light
import importlib, sys as _sys
importlib.invalidate_caches()
import qiskit_metal
print("qiskit_metal from:", qiskit_metal.__file__)
assert qiskit_metal.__file__.startswith(str(pkg)), "Not importing from /content/qiskit-metal!"
```

| Quantum Chip Rendering Steps: |
| - |
| [Qiskit Metal + KLayout + Blender](https://youtu.be/NxArWX8WhPc?si=C-xPu6bjvJBSJs_t) |

---

| Required Software (Some Free, Open-Sourced Versions Are Linked Below): |
| - |
| Qiskit Metal |
| 2D CAD program |
| Pattern layout viewer & editor (GDS-to-DXF/DXF-to-GDS converter) |
| Electron- & LASER-beam lithography software (GDS-to-GPF converter for equipment) |


| 2D CAD Programs Available: | Description |
| - | - |
| AutoCAD or AutoCAD Web | Cost effective alternative to locally-installed AutoCAD: <br> <https://www.autodesk.com/products/autocad-web/overview?term=1-YEAR&tab=subscription&plc=A360PP> |
| QCAD | Open-sourced & simple: <br> <https://qcad.org/en> |
| LibreCAD | Open-sourced & feature-packed: <br> <https://librecad.org> |
| FreeCAD | Open-sourced & feature-packed: <br> <https://www.freecad.org> |
| Salome | Open-sourced & feature-packed: <br> <https://www.salome-platform.org/?page_id=2430> |

| Pattern Layout Viewers & Editors: | Description |
| - | - |
| KLayout | Open-sourced & feature-packed: <br> <https://www.klayout.de/build.html> |
| LinkCAD | Paid version: <br> <https://www.linkcad.com/download.php> [usually purchased by your lab] |
| Raith_GDSII MATLAB Toolbox | Public licensed <br> <https://github.com/ahryciw/Raith_GDSII> |
| Octave/ MATLAB Toolbox for GDSII | Public domain: <br> <https://github.com/ulfgri/gdsii-toolbox> |

| Free or Open-Source Software for Design, Analysis, or Large Data Visualization: |
| - |
| <https://dev.opencascade.org/about/projects_and_products> |
| <https://www.paraview.org/download> |

| Open-Source Finite Element Method Software (Alternative to Ansys): |
| - |
| <https://github.com/ElmerCSC/elmerfem> |

| Open-Source Mesh Generators (To Prepare Design for Use in Finite Element Method Software): |
| - |
| <https://gmsh.info/#Download> |
| <https://www.salome-platform.org/?page_id=2430> |

| Open-Source Device Simulation Tools: |
| - |
| <https://gdsfactory.github.io/gdsfactory/plugins_process.html> |

| Electron- & LASER-Beam Lithography Software: |
| - |
| BEAMER (from GenIsys: <https://www.genisys-gmbh.com/beamer.html> [usually purchased by your lab]) |

| Slides & Webinars for Using Electron-Beam Lithography Software: |
| - |
| <https://www.genisys-gmbh.com/webinar-series-beamer-training.html> |

| General Overview of Electron-Beam Lithography + Highlights: |
| - |
| <https://nano.yale.edu/book/export/html/213> |
| <https://ebeam.mff.uw.edu/ebeamweb/doc/doc/overview.html> |
| <https://ebeam.mff.uw.edu/ebeamweb/news/projects/index.html> |
| <https://apps.mnc.umn.edu/archive/ebpgwiki/SOP.html> |
| <https://nano.yale.edu/tips-and-tricks-ebeam-users> |
| <https://nano.yale.edu/manuals-documentation> |
| <https://ebeam.mff.uw.edu/ebeamweb/doc/doc/overview.html> |

| Documentation & Resources for 4 Common Electron-Beam Lithography Machines: |
| - |
| Elionix ELS-7500EX E-Beam Lithography System: <br> <https://wiki.nano.upenn.edu/wiki/index.php?title=Elionix_ELS-7500EX_E-Beam_Lithography_System> |
| Raith EBPG 5200+ E-Beam Lithography System: <br> <https://wiki.nano.upenn.edu/wiki/index.php?title=Elionix_ELS-7500EX_E-Beam_Lithography_System> | 
| Raith EBPG 5200 E-Beam Lithography System: <br> <https://lab.kni.caltech.edu/index.php/EBPG_5200:_100_kV_Electron_Beam_Lithography> |
| Raith EBPG 5000+ E-Beam Lithography System: <br> <https://lab.kni.caltech.edu/EBPG_5000%2B:_100_kV_Electron_Beam_Lithography> |

| Documentation & Resources for a Common LASER Direct-Write Lithography Machine: |
| - |
| Heidelberg DWL-66 Direct-Write Laser Lithography System: <br> <https://lab.kni.caltech.edu/DWL-66:_Direct-Write_Laser_System> |

| List of Available Process Recipes: |
| - |
| <https://lab.kni.caltech.edu/Process_Recipe_Library> |
| <https://nano.yale.edu/manuals-documentation> |

| Open-Source Computational Lithography Tools: |
| - |
| <https://github.com/looninho/CUDAEBL> |
| <https://github.com/pierremifasol/Lithography-Simulation> |
| <https://github.com/lani5677/Computational-lithography> |

| Examples of Green [Sustainable] Lithography-Based Direct-Write Patterning: |
| - |
| <https://onlinelibrary.wiley.com/doi/full/10.1002/admi.201601223> |
| <https://onlinelibrary.wiley.com/doi/10.1002/adfm.202101533> |

| List of Standard Negative/ Positive Tone Resist Materials: |
| - |
| <https://www.microresist.de/en/products/?jet-smart-filters=jet-engine/products&_tax_query_pa_resist-alliance=534> |
| <https://www.epfl.ch/about/campus/neuchatel-en/daily-life/page-119059-en-html/page-126398-en-html> |

| List of Open-Source Process Development Kits & More (Optional): |
| - |
| SiEPIC Ebeam PDK: <https://gdsfactory.github.io/ubc> |
| Skywater 130 PDK: <https://gdsfactory.github.io/skywater130> |
| GlobalFoundries 180 PDK: <https://gdsfactory.github.io/gf180> |
| Python library to design chips [Photonics, Analog, Quantum, MEMs, etc.]: <https://github.com/gdsfactory/gdsfactory> |

---

| Some of the Code Used Here are Borrowed or Inspired From the Qiskit Metal Page: |
| - |
| <https://github.com/qiskit-community/qiskit-metal> |

---

## To create the chip below, follow tutorials from the folder called "[Python Code_Qiskit Metal_Designs](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/tree/main/Python%20Code_Qiskit%20Metal_Designs)" on main branch in this repository. Afterwards, proceed to a file called "[Transmon Chip Fabrication Process Flow](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/blob/main/Transmon%20Chip%20Fabrication%20Process%20Flow.pdf)", also on the main branch. (Optionally, click on both hyperlinks to find the tutorials).

---

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/a8553658-9b1f-4c46-a6c2-fdcef7639d29)

![20230616_065853](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/604e6ff1-006b-4aa5-a61d-2b3a3a65e7dc)

![20230616_065902_c](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/6397d09e-f97a-4316-a753-73f5132e409e)

![249468107-5d549f3e-53bb-4b9d-8056-8a0564af98f9](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/ec7fb884-9080-4c12-8b05-b61de7151f7d)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/a7396b69-4c91-47be-a736-327b168a9f14)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/9c5d1fa1-79f4-4053-988c-373e1bdae512)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/22c77ca7-1453-4e55-a6c3-bdca0a19cdd6)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/438d5883-2c8e-4230-8fa8-9f43d0bec9b8)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/136c6ce6-568a-4477-ad70-89df4ee516ab)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/8e46ee3b-b6c8-4299-ac25-240d0c12dc26)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/679f9a63-9e80-4596-aede-5fd9b0ab72ed)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/93227874-124c-4736-802e-37d5e365dc7a)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/d2b6ae6b-03e3-4483-8e76-7ea20c6aeb34)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/6993c29a-9c02-4b7c-98f8-3cddacab0ee0)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/38c5a780-264f-42a7-8bd4-31179b3224ac)

### Onri's Trilayer Tunnel Junction Process (Cross-Sectional View):

![image](https://github.com/user-attachments/assets/18d406f4-337f-4468-bfc5-b1d0d262c064)

![Fibonacci Word Fractal Lines_80 nm](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/dd72498d-2067-451c-bba7-dafe6165f292)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/blob/main/OJB_Quantum_System.gif)
