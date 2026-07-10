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

    # Pre-import ALL stdlib modules to prevent "No module named" errors
    # PaddlePaddle dynamically imports many stdlib submodules at runtime
    import importlib
    import pkgutil

    # First pass: all top-level stdlib packages (import only, skip heavy ones)
    _skip = {
        'tkinter', 'test', 'unittest',  # GUI/testing (already handled)
        'antigravity', 'this',           # interactive/joke modules
        'distutils', 'setuptools',      # packaging (included separately)
        'ensurepip', 'pip', 'wheel',    # package managers
        'pydoc', 'pydoc_data',          # documentation
        'idlelib', 'lib2to3',           # dev tools
        'zoneinfo',                      # timezone (rarely needed)
        '__pycache__', '__future__',
    }

    for finder, modname, ispkg in pkgutil.iter_modules():
        if ispkg and modname not in _skip:
            try:
                importlib.import_module(modname)
            except Exception:
                pass

    # Second pass: known submodules that pkgutil misses
    _submodules = [
        # logging
        'logging.handlers', 'logging.config', 'logging.handlers.QueueHandler',
        # xml
        'xml.etree.ElementTree', 'xml.etree.cElementTree',
        'xml.dom', 'xml.dom.minidom', 'xml.dom.pulldom',
        'xml.parsers.expat', 'xml.sax', 'xml.sax.saxutils',
        'xml.sax.handler', 'xml.sax.xmlreader',
        # urllib
        'urllib.parse', 'urllib.request', 'urllib.error',
        'urllib.response', 'urllib.robotparser',
        # http
        'http.client', 'http.server', 'http.cookiejar',
        'http.cookies', 'http.cookiejar',
        # email
        'email.utils', 'email.parser', 'email.policy',
        'email.mime', 'email.mime.text', 'email.mime.multipart',
        'email.mime.base', 'email.mime.image', 'email.header',
        'email.headerregistry', 'email.iterators', 'email.message',
        'email.charset', 'email.encoders', 'email.errors',
        'email.contentmanager', 'email.generator',
        # importlib
        'importlib.metadata', 'importlib.resources',
        'importlib.abc', 'importlib.machinery',
        # ctypes
        'ctypes.wintypes', 'ctypes.util', 'ctypes._endian',
        # collections
        'collections.abc', 'collections.defaultdict', 'collections.ordereddict',
        # concurrent
        'concurrent.futures', 'concurrent.futures.thread',
        'concurrent.futures.process',
        # audio / video (used by paddle model loading)
        'wave', 'aifc', 'sunau', 'audioop',
        'chunk', 'colorsys',
        # misc
        'pathlib', 'tempfile', 'shutil', 'fileinput', 'filecmp',
        'fnmatch', 'glob', 'stat', 'filelock',
        'argparse', 'configparser', 'csv', 'ssl', 'hashlib',
        'hmac', 'secrets', 'base64', 'binascii',
        'decimal', 'fractions', 'numbers', 'random',
        'pprint', 'reprlib', 'textwrap',
        'struct', 'codecs', 'unicodedata', 'locale',
        'calendar', 'datetime', 'timeit', 'sched',
        'threading', 'queue', 'thread', '_thread',
        'multiprocessing', 'multiprocessing.connection',
        'multiprocessing.process', 'multiprocessing.queue',
        'multiprocessing.reduction', 'multiprocessing.shared_memory',
        'multiprocessing.managers', 'multiprocessing.pool',
        'subprocess', 'signal', 'mmap', 'msvcrt',
        'socket', 'select', 'selectors', 'asyncio',
        'ssl', 'ipaddress', 'uuid',
        'json', 'csv', 'plistlib', 'netrc',
        'sqlite3', 'dbm', 'dbm.dumb', 'dbm.gnu', 'shelve',
        'lzma', 'bz2', 'gzip', 'zipfile', 'zlib', 'zlib.compress',
        'tarfile', 'tempfile',
        'io', 'os', 'os.path', 're', 'math', 'cmath',
        'operator', 'itertools', 'functools', 'functools.partial',
        'copy', 'copyreg', 'weakref', 'types',
        'pickle', 'shelve', 'marshal', 'shlex',
        'tokenize', 'keyword', 'token', 'symbol',
        'dis', 'opcode', 'code', 'codeop', 'compile',
        'ast', 'symtable', 'inspect', 'platform',
        'traceback', 'linecache', 'trace', 'tracemalloc',
        'gc', 'resource', 'syslog',
        'abc', 'numbers', 'enum', 'typing', 'typing_extensions',
        'dataclasses', 'contextvars', 'contextlib',
        'warnings', 'contextlib',
        'atexit', 'posixpath', 'ntpath', 'genericpath',
        'posix', 'nt',
        '_collections_abc', '_abc', '_functools',
    ]
    for mod_name in _submodules:
        try:
            importlib.import_module(mod_name)
        except Exception:
            pass
