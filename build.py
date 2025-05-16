import PyInstaller.__main__
import PyInstaller.config
import shutil
import os

PyInstaller.__main__.run([
  "main.py", 
  "--name", "InfoCuboFunctionality", 
  "--noconsole", 
  "--icon=cube.ico",
  "--version-file", "version.txt" 
])

#COPYING INDEX TABLE
if not os.path.exists("dist/InfoCuboFunctionality/data/"):
  os.makedirs("dist/InfoCuboFunctionality/data/")
shutil.copyfile("data/indexTable.csv", "dist/InfoCuboFunctionality/data/indexTable.csv")