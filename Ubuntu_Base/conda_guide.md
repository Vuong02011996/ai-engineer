# Basic command
+ Create new: `conda create --name name_venv python=3.8`
+ Activate : `conda activate name_venv`
+ List all conda environments: `conda info --envs`
+ List all installed packages:  `conda list`
+ Remove one: `conda env remove --name myenv`
+ Install cuda in conda: `conda install -c anaconda cudatoolkit=10.1`
+ Create file requirements:  `conda list -e > requirements.txt OR pip freeze > requirements.txt`