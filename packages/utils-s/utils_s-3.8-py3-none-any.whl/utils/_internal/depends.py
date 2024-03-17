import importlib
import subprocess
import sys


def attemptImport(packagePythonName, packagePip3Name):

    def importFunction():
        return importlib.import_module(name=packagePythonName)

    try:
        return importFunction()
    except (ImportError, ModuleNotFoundError):

        if sys.version_info.minor < 12:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', packagePip3Name], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', packagePip3Name, '--break-system-packages'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    return importFunction()
