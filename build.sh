pyinstaller gui_qt5.py
rm -r gui_qt5.spec build/ __pycache__/
ln -s dist/gui_qt5/gui_qt5 . 