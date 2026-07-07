# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec - VSE Win7 Standalone Build"""
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

PROJECT_ROOT = os.path.dirname(os.path.abspath(SPEC))

# Collect PySide6 data
pyside6_datas, pyside6_bins, pyside6_hidden = collect_all('PySide6')
# Collect paddle + paddleocr data
paddle_datas = collect_data_files('paddleocr')
paddle_hidden = collect_submodules('paddle')
paddle_hidden += collect_submodules('paddleocr')
# Collect qfluentwidgets data
qfw_datas = collect_data_files('qfluentwidgets')
# Collect qframelesswindow
qfw_datas += collect_data_files('PySide6-Frameless-Window')
# Collect pytz for Win7 compat
pytz_datas, pytz_bins, pytz_hidden = collect_all('pytz')

added_files = [
    (os.path.join(PROJECT_ROOT, 'backend'), 'backend'),
    (os.path.join(PROJECT_ROOT, 'design'), 'design'),
    (os.path.join(PROJECT_ROOT, 'ui'), 'ui'),
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'gui.py')],
    pathex=[PROJECT_ROOT],
    binaries=pyside6_bins + pytz_bins,
    datas=added_files + pyside6_datas + paddle_datas + qfw_datas + pytz_datas,
    hiddenimports=[
        'paddle', 'paddle.fluid', 'paddleocr', 'paddle.vision',
        'cv2', 'numpy', 'PIL', 'yaml', 'requests', 'tqdm',
        'loguru', 'shapely', 'lanms', 'pyclipper',
        'qfluentwidgets', 'qframelesswindow',
        'PySide6', 'PySide6.QtCore', 'PySide6.QtWidgets',
        'PySide6.QtGui', 'PySide6.QtNetwork',
        'je_showinfilemanager',
        'imageio_ffmpeg',
    ] + paddle_hidden + pyside6_hidden + pytz_hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'scipy', 'IPython', 'jupyter', 'notebook',
        'pytest', 'sphinx', 'pip', 'wheel', 'selenium',
        'unittest', 'pydoc', 'xmlrpc', 'pydoc_data',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VideoSubtitleExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(PROJECT_ROOT, 'design', 'vse.ico'),
)
