from . import _version
__version__ = _version.get_versions()['version']

try:
    import pyolite
    import pyodide
except Exception:
    pass

def pyoliteutilsinfo():
    try:
        print("pyoliteutils=", __version__, "pyodide=", pyodide.__version__, "pyolite=", pyolite.__version__)
    except Exception:
        print("pyoliteutils=", __version__)

