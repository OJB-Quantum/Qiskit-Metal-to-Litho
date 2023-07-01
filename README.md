# Qiskit-Metal-to-Litho
On the use of Qiskit Metal coded in Python to generate design files for building quantum devices on a chip, performed via direct-write lithography. Depending on the resolution of desired quantum device features, LASER, scanning thermal probe, and electron-beam techniques are applicable options for patterning your design.

(Note: in the patterned 400-transmon example below, the ground contacts were excluded from layout as the design was to demonstrate process feasibility from Qiskit Metal design-to-real-chip. However, the main features are clearly visible under optical microscopy. Also, I included a DXF/GDS design output for a full quantum chip ready for fabrication [electrodes, ground, and all], available to download in the file directories above).

![20230616_081944](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/7c20c740-19f3-4a0e-b471-a6ab591f89c0)

## It is important to know that there are 2 main types of patterning with the e-beam writer (EBPG) equipment: 
- (Marker-based using "rp" commands) - this is used if your sample has pre-existing markers patterned on it already [ex. sample WITH purposely-designed reference points that can be automatically located by the EBPG's built-in SEM tool].
- (Marker-free-based using "joyplus" commands) - this is used if your sample has no pre-existing referencing patterns [ex. bare substrate or other sample WITHOUT purposely-designed reference points].

## Terms to be aware of:
- BEAMER - Desktop software for importing GDSII or GDS files stored on WinSCP, beam step, size, and error correction (heal) paramters are set here and subsequently exported as GPF files that can be read by the EBPG equipment. Additionally the parameters can be downloaded as a Python script (.py). An example of a Python script used in BEAMER is available for reference in the file directory above.
- CJOB - Software tool that is accessed on the EBPG equipment itself using the EBPG's terminal. From here, the GPF files can be uploaded and programmed with virtual alignment marker locations based on the uploaded design. Once the file is ready, it will export as a JOB file (.job). The JOB file name is what gets copied into the EBPG's terminal along with 4 coordinates validated by the built-in SEM.


## Required software (some open-source free versions will be linked below):
- Qiskit Metal
- 2D CAD program
- Pattern layout viewer & editor (GDS-to-DXF/DXF-to-GDS converter)
- Electron- and LASER-beam lithography software (GDS-to-GPF converter for equipment)

## Installation steps for Qiskit Metal can be found in the "requirements_plus" folder stored on this repository.


### 2D CAD programs available:
- AutoCAD or AutoCAD Web (cost effective alternative to locally-installed AutoCAD: https://www.autodesk.com/products/autocad-web/overview?term=1-YEAR&tab=subscription&plc=A360PP)
- QCAD (open-sourced and simple: https://qcad.org/en)
- LibreCAD (open-sourced and feature-packed: https://librecad.org)

### Pattern layout viewers & editors:
- LinkCAD (paid version: https://www.linkcad.com/download.php [usually purchased by your lab])
- KLayout (open-sourced & feature-packed: https://www.klayout.de/build.html)
- Raith_GDSII MATLAB Toolbox (public licensed: https://github.com/ahryciw/Raith_GDSII)
- Octave/ MATLAB Toolbox for GDSII (public domain: https://github.com/ulfgri/gdsii-toolbox)

### Electron- and LASER-beam lithography software:
- BEAMER (from GenIsys: https://www.genisys-gmbh.com/beamer.html [usually purchased by your lab])

### Slides and webinars for using electron-beam lithography software:
- https://www.genisys-gmbh.com/webinar-series-beamer-training.html

### General overview of electron-beam lithography:
- https://nano.yale.edu/book/export/html/213
- https://lab.kni.caltech.edu/EBPG_5000%2B:_100_kV_Electron_Beam_Lithography

### Examples of green lithography-based direct-write patterning:
- https://onlinelibrary.wiley.com/doi/full/10.1002/admi.201601223
- https://onlinelibrary.wiley.com/doi/10.1002/adfm.202101533

### List of standard negative/ positive resist materials:
- https://www.microresist.de/en/products/?jet-smart-filters=jet-engine/products&_tax_query_pa_resist-alliance=534
- https://www.epfl.ch/about/campus/neuchatel-en/daily-life/page-119059-en-html/page-126398-en-html

### List of available process recipes:
- https://lab.kni.caltech.edu/Process_Recipe_Library
_________________________________________________________________________________________________________________________________________________
### Some of the code used here are borrowed or inspired from the Qiskit Metal page: 
- https://github.com/qiskit-community/qiskit-metal/tree/main
_________________________________________________________________________________________________________________________________________________
### To create the chip below, follow the design process flow from the folder called "Python Code_Qiskit Metal_Designs" in this repository.
_________________________________________________________________________________________________________________________________________________

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/a8553658-9b1f-4c46-a6c2-fdcef7639d29)

![20230616_065853](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/604e6ff1-006b-4aa5-a61d-2b3a3a65e7dc)

![20230616_065902_c](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/6397d09e-f97a-4316-a753-73f5132e409e)

![249468107-5d549f3e-53bb-4b9d-8056-8a0564af98f9](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/ec7fb884-9080-4c12-8b05-b61de7151f7d)





![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/136c6ce6-568a-4477-ad70-89df4ee516ab)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/8e46ee3b-b6c8-4299-ac25-240d0c12dc26)

![image](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/679f9a63-9e80-4596-aede-5fd9b0ab72ed)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/93227874-124c-4736-802e-37d5e365dc7a)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/d2b6ae6b-03e3-4483-8e76-7ea20c6aeb34)

![unnamed](https://github.com/OJB-Quantum/Qiskit-Metal-to-Litho/assets/88035770/6993c29a-9c02-4b7c-98f8-3cddacab0ee0)


