18/01/24: Problems with virtual environment and xgboost: Module not found error
pip list and examining the venv folder would reveal that xgboost was downloaded. Repeated installs did not work as it was already available, even if it was installed within the notebook (i.e. !pip install xgboost) 

Fix occurred after:
1. Manually creating a new venv and selecting the file path which was recommended. Currently the kernel is in here: "C:\Users\z5291979\OneDrive - UNSW\Documents\lsac-data\lsac-suicidality\.venv\Scripts\python.exe". 

Redownload all requirements as recommended by VSCode. Try to make sure the file paths line up.
2. conda install xgboost in Anaconda Navigator's Powershell:
 (condaenv) PS C:\Users\z5291979> conda install xgboost
This was installed into the conda environment- though I am using a venv not a conda environment. Logically this shouldn't work, but if all else fails just try it.