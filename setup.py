from cx_Freeze import setup, Executable
import sys
import os.path

# python -m venv myenv
# pip ile gerekli kutuphanleri yukle
# myenv\Scripts\activate
# python setup.py build_exe


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = {
    'packages': ['os', 'numpy', 'matplotlib', 'PyQt6', 'yaml'],
    'include_files': [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
    ],
    'excludes': ['tkinter']
}

setup(
    name="LogIncelemeArayuzu",
    version="3.7",
    description="Log İnceleme Arayüzü, Ahmet Yasin CIVAN, 2023",
    options={"build_exe": build_exe_options},
    executables=[Executable("log_inceleme_arayuzu.py", base=base,
                            icon="icon.ico")]
)
