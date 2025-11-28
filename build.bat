@echo off
echo Building Beerkart App...
pyinstaller --onefile --windowed --icon=./assets/beer.ico --name=Beerkart_App_V1.0 --add-data="assets;assets" main.py
echo Build complete!
pause