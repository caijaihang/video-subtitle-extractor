# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec - VSE Win7 Standalone Build"""
import os
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
# Collect qframelesswindow data (actual PyPI package name)
qfw_datas += collect_data_files('PySideSix_Frameless_Window')
# Collect pytz for timezone support
pytz_datas, pytz_bins, pytz_hidden = collect_all('pytz')
# Collect darkdetect for theme detection
darkdetect_datas, darkdetect_bins, darkdetect_hidden = collect_all('darkdetect')
# Collect imageio_ffmpeg for sushi module
imageio_ff_datas = collect_data_files('imageio_ffmpeg')

added_files = [
    (os.path.join(PROJECT_ROOT, 'backend'), 'backend'),
    (os.path.join(PROJECT_ROOT, 'design'), 'design'),
    (os.path.join(PROJECT_ROOT, 'ui'), 'ui'),
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'gui.py')],
    pathex=[PROJECT_ROOT],
    binaries=pyside6_bins + pytz_bins + darkdetect_bins,
    datas=added_files + pyside6_datas + paddle_datas + qfw_datas + pytz_datas + imageio_ff_datas,
    hiddenimports=[
        # PaddlePaddle / PaddleOCR
        'paddle', 'paddle.fluid', 'paddleocr', 'paddle.vision',
        'paddleocr.text_detection',
        # CV
        'cv2', 'numpy', 'PIL',
        # Internal modules
        'backend', 'backend.config', 'backend.main',
        'backend.bean', 'backend.bean.subtitle_area',
        'backend.tools', 'backend.tools.ocr', 'backend.tools.constant',
        'backend.tools.hardware_accelerator', 'backend.tools.paddle_model_config',
        'backend.tools.process_manager', 'backend.tools.subtitle_detect',
        'backend.tools.subtitle_ocr', 'backend.tools.reformat',
        'backend.tools.theme_listener', 'backend.tools.version_service',
        'backend.tools.subtitle_extractor_remote_call',
        'backend.tools.python_runner', 'backend.tools.concurrent',
        'backend.tools.concurrent.task', 'backend.tools.concurrent.task_manager',
        'backend.tools.concurrent.future',
        'backend.sushi', 'backend.sushi.sushi_main', 'backend.sushi.subs',
        'ui', 'ui.home_interface', 'ui.setting_interface',
        'ui.advanced_setting_interface', 'ui.timeline_sync_interface',
        'ui.component', 'ui.component.video_display_component',
        'ui.component.task_list_component',
        'ui.icon', 'ui.icon.my_fluent_icon',
        # Third-party
        'qfluentwidgets', 'qframelesswindow', 'qframelesswindow.utils',
        'darkdetect', 'chardet',
        'yaml', 'requests', 'tqdm', 'loguru', 'shapely', 'pyclipper',
        'pysrt', 'wordsegment', 'lmdb', 'skimage',
        'je_showinfilemanager', 'imageio_ffmpeg',
        'Levenshtein',
        # PySide6
        'PySide6', 'PySide6.QtCore', 'PySide6.QtWidgets',
        'PySide6.QtGui', 'PySide6.QtNetwork', 'PySide6.QtMultimedia',
    ] + paddle_hidden + pyside6_hidden + pytz_hidden + darkdetect_hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'scipy', 'IPython', 'jupyter', 'notebook',
        'pytest', 'sphinx', 'pip', 'wheel', 'selenium',
        'unittest', 'pydoc', 'xmlrpc', 'pydoc_data',
        'tkinter', 'test', 'tests',
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
