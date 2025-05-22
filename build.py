import os
import shutil

import PyInstaller.__main__
import PyInstaller.config

PyInstaller.__main__.run([
  "main.py", 
  "--name", "InfoCuboFunctionality", 
  "--noconsole", 
  "--icon=cube.ico",
  "--version-file", "version.txt",
  "--add-data", "logs;logs",
  "--add-data", "data;data" 
])

#COPYING INDEX TABLE
if not os.path.exists("dist/InfoCuboFunctionality/data/"):
  os.makedirs("dist/InfoCuboFunctionality/data/")
shutil.copyfile("data/indexTable.csv", "dist/InfoCuboFunctionality/data/indexTable.csv")