@echo off
echo starting python install, it might take up to 10 minutes
python-3.8.2.exe /passive /InstallAllUsers=1 /Include_launcher=0 InstallLauncherAllUsers=0 /Include_pip=1
echo starting additional binaries install, it requires internet connection.
pip install -r requirements.txt
echo finished installing
