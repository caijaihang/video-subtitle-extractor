"""
PyInstaller runtime hook - VSE Win7
Ensures correct paths for models, configs, and working directories
when running as a packaged application.
"""
import sys
import os

if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    temp_dir = sys._MEIPASS

    # Set working directory to EXE location (needed for config, cache, output files)
    os.chdir(exe_dir)

    # Ensure config directory exists (for config.json)
    config_dir = os.path.join(exe_dir, 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Ensure output directory for cache/frames exists
    for subdir in ['loss', 'cache']:
        d = os.path.join(exe_dir, subdir)
        if not os.path.exists(d):
            os.makedirs(d)

    # Copy models from _MEIPASS if not present in EXE directory
    # (Models are large; keeping them beside EXE avoids _MEIPASS bloat)
    models_src = os.path.join(temp_dir, 'backend', 'models')
    models_dst = os.path.join(exe_dir, 'backend', 'models')
    if not os.path.exists(models_dst) and os.path.exists(models_src):
        import shutil
        shutil.copytree(models_src, models_dst)
        print(f'[Runtime] Copied models to {models_dst}')
