# eChem

A suite of helper tools to manipulate results from electrochemical measurements such as linear sweep voltammetry (LSV) and electrochemical impedance spectroscopy (EIS). The tools include a Wolfram Mathematica package (eChem.m) and a separate Python tool (importLSV.py). 

## eChem.m
The Wolfram Mathematica package (`eChem.m`) contains the following functions:
* **`importEIS`**: This function imports multiple Electrochemical Impedance Spectroscopy (EIS) data from text files (typically comma-separated CSV files). It can output data in a format suitable for plotting with e.g. `showEIS`, or in a tabular format suitable for interfacing with the [`ChemPattern`](https://github.com/mabonizzoni/ChemPattern) suite of functions for chemical pattern recognition and analysis. Returns an Association where keys are bias voltages and values are the raw impedance data matrices.

* **`showEIS`**: This function creates an interactive visualization tool for exploring EIS datasets allowing the user to select which datasets to display (with consistent color coding), choose bias voltage, and pick variables to present on the vertical and horizontal axes among frequency, Z', Z", |Z|, and phase. The user can also interactively apply logarithmic, linear, or reversed scaling to either axis independently.



## importLSV.py
Python code relying only on the Python Standard Library to re-format results from multiple linear sweep voltammetry (LSV) experiments carried out over the same range of potentials into a single table. In the resulting table, the first column is potential (in volts, V), and the following columns correspond to currents (in amperes A) for each experimental run. 
