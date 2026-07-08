"""
PyInstaller runtime hook - VSE Win7
Ensures correct paths for models, configs, working directories, and Win7 compat
"""
import sys
import os

if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    temp_dir = sys._MEIPASS
    internal_dir = os.path.join(exe_dir, '_internal')

    # Add _internal to DLL search path (Windows)
    if sys.platform == 'win32' and hasattr(os, 'add_dll_directory'):
        try:
            os.add_dll_directory(internal_dir)
        except Exception:
            pass
        # Also add EXE directory for Win7 shim DLLs
        try:
            os.add_dll_directory(exe_dir)
        except Exception:
            pass

    # Set working directory to EXE location
    os.chdir(exe_dir)

    # Ensure writable directories exist
    for subdir in ['config', 'loss', 'cache', 'output']:
        d = os.path.join(exe_dir, subdir)
        if not os.path.exists(d):
            os.makedirs(d)
