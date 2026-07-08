# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec - VSE Win7 Build (onedir, PyQt5 + PaddlePaddle)"""
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

PROJECT_ROOT = os.path.dirname(os.path.abspath(SPEC))

# Collect PyQt5 (Qt5 - Win7 compatible)
pyqt5_datas, pyqt5_bins, pyqt5_hidden = collect_all('PyQt5')

# Collect PyQt-Fluent-Widgets (PyQt5 version of qfluentwidgets)
qfw_datas, qfw_bins, qfw_hidden = collect_all('qfluentwidgets')
# PyQt5-Frameless-Window provides qframelesswindow module
qframe_datas, qframe_bins, qframe_hidden = collect_all('PyQt5_Frameless_Window')

# Collect PaddlePaddle + PaddleOCR
paddle_datas, paddle_bins, paddle_hidden = collect_all('paddle')
paddleocr_datas, paddleocr_bins, paddleocr_hidden = collect_all('paddleocr')

# Utility packages
pytz_datas, pytz_bins, pytz_hidden = collect_all('pytz')
darkdetect_datas, darkdetect_bins, darkdetect_hidden = collect_all('darkdetect')
imageio_ff_datas, imageio_ff_bins, imageio_ff_hidden = collect_all('imageio_ffmpeg')

# Win7 shim DLL
win7_compat_dir = os.path.join(PROJECT_ROOT, 'win7_compat')
win7_bins = [(os.path.join(win7_compat_dir, f), '.') for f in os.listdir(win7_compat_dir) if f.endswith('.dll')]

# Project files
added_files = [
    (os.path.join(PROJECT_ROOT, 'backend'), 'backend'),
    (os.path.join(PROJECT_ROOT, 'design'), 'design'),
    (os.path.join(PROJECT_ROOT, 'ui'), 'ui'),
]

all_binaries = (pyqt5_bins + qfw_bins + qframe_bins + paddle_bins + paddleocr_bins
                 + pytz_bins + darkdetect_bins + imageio_ff_bins + win7_bins)
all_datas = (added_files + pyqt5_datas + qfw_datas + qframe_datas + paddle_datas
             + paddleocr_datas + pytz_datas + darkdetect_datas + imageio_ff_datas)

all_hidden = ([
    'paddle', 'paddle.fluid', 'paddleocr', 'paddle.vision',
    'cv2', 'numpy', 'PIL', 'imageio', 'skimage',
    # Internal
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
    'pysrt', 'wordsegment', 'lmdb',
    'je_showinfilemanager', 'imageio_ffmpeg', 'Levenshtein',
    # PyQt5
    'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtWidgets',
    'PyQt5.QtGui', 'PyQt5.QtNetwork',
] + paddle_hidden + paddleocr_hidden + pyqt5_hidden + qfw_hidden
    + qframe_hidden + pytz_hidden + darkdetect_hidden + imageio_ff_hidden)

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'gui.py')],
    pathex=[PROJECT_ROOT],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    runtime_hooks=[os.path.join(PROJECT_ROOT, 'hook-runtime.py')],
    excludes=[
        'matplotlib', 'scipy', 'IPython', 'jupyter', 'notebook',
        'pytest', 'sphinx', 'pip', 'wheel', 'selenium',
        'unittest', 'pydoc', 'xmlrpc', 'pydoc_data',
        'tkinter', 'test', 'tests',
        'PySide6', 'PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui',
        'PySideSix_Frameless_Window',
        'paddle.vision.models', 'paddle.text', 'paddle.audio',
        'paddle.quantization', 'paddle.sparse',
        'paddle.fluid.contrib', 'paddle.fluid.layers',
        'paddle.distributed', 'paddle.incubate',
        'paddle.hapi',
        'modelscope', 'transformers', 'fairseq', 'torch', 'torchvision',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoSubtitleExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(PROJECT_ROOT, 'design', 'vse.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='VideoSubtitleExtractor',
)
