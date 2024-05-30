# Install

```commandline
#rm -rf ~/anaconda3 ~/.condarc ~/.conda ~/.continuum
#sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 -y
#wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
#sha256sum /tmp/Anaconda3-2020.02-Linux-x86_64.sh
#bash /tmp/Anaconda3-2020.02-Linux-x86_64.sh -y
#source /home/$USER/.bashrc
#conda config --set auto_activate_base false

Error: conda not init - set PATH
https://saturncloud.io/blog/solving-the-conda-command-not-found-issue-after-installing-anaconda3/
```


# Using 
```commandline
conda create --name name_venv python
conda activate name_venv
conda create --name name_venv python=3.8
conda info --envs
conda list
conda env remove --name myenv
conda install -c anaconda cudatoolkit=10.1
```
