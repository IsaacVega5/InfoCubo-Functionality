import PyInstaller.__main__
import PyInstaller.config

PyInstaller.__main__.run([
  "main.py", 
  "--name", "InfoCuboFunctionality", 
  "--onefile", 
  "--noconsole", 
  "--icon=cube.ico",
  "--version-file", "version.txt"                        
])