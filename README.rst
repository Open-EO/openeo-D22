=============
D22 scripts
=============


This repository contains a set of scripts to run an EVI job on multiple back-ends. It also includes a Jupyter notebook to check the results and create some combined plots which feed into Deliverable D22.

RGB previews of the data involved in this job are avalibale in the RGB_previews/ folder.

To use the scripts follow the steps below.


1. Back-ends' credentials
-------------------------

Copy the file 'backends_auth_sample' to 'backends_auth' and fill in the credentials for each back-end.

2. Run main.py
--------------

You can select inside 'main.py' which back-ends to connect to. The script for each back-end is in the scripts/ folder.
The output is saved in the results/ folder (existing files will be overwritten.)

3. Run Jupyter notebook
-----------------------------------------------------------------------------------

Run the 'compare_outputs' Jupyter notebook to create plots and see some statistics about the output results. You need to select 'L1C' or 'L2A' in the notebook.
The output is stored in the comparison_output/ folder.
