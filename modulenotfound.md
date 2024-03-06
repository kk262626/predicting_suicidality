6/03/24: Problems again with module not found error 
I think I have found the fix for real this time. When I entered 'where pip' in the terminal, it was installing into the global environment rather than the venv activated in the notebook. I've created a new environment for this project- 26env for all of the packages to be installed into.

Make sure to start off by activating the venv in the terminal:
Run this in cmd: 26venv\Scripts\activate
Then pip install -r requirements.txt into the right venv
Make sure your notebook is also running from 26venv

If this problem occurs again and you need to start afresh with a new venv, follow these steps:
https://saturncloud.io/blog/how-to-set-up-virtual-environments-in-visual-studio-code-for-jupyter-notebooks/
Basically, create a new environment in the terminal: python -m venv <name_of_virtual_environment>
And then activate as above

18/01/24: Problems with virtual environment and xgboost: Module not found error
pip list and examining the venv folder would reveal that xgboost was downloaded. Repeated installs did not work as it was already available, even if it was installed within the notebook (i.e. !pip install xgboost) 

Fix occurred after:
1. Manually creating a new venv and selecting the file path which was recommended. Currently the kernel is in here: "C:\Users\z5291979\OneDrive - UNSW\Documents\lsac-data\lsac-suicidality\.venv\Scripts\python.exe". 

Redownload all requirements as recommended by VSCode. Try to make sure the file paths line up.
2. conda install xgboost in Anaconda Navigator's Powershell:
 (condaenv) PS C:\Users\z5291979> conda install xgboost
This was installed into the conda environment- though I am using a venv not a conda environment. Logically this shouldn't work, but if all else fails just try it.