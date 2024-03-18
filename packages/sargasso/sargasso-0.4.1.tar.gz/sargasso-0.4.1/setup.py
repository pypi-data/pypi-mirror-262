import os
import setuptools
from glob import glob
from pybind11.setup_helpers import Pybind11Extension, build_ext

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PACKAGE_DIR, "src")

SRC_PATHS = list(
    map(
        lambda p: os.path.join(SRC_DIR, p),
        [
            "funcs.cpp",
            "module.cpp",
        ],
    )
)

INCLUDE_DIRS = [os.path.join(PACKAGE_DIR, "include")]
LIBRARY_DIRS = []

INCLUDE_DIRS_TO_SEARCH = [
    "/usr/include",
    "/usr/include/openblas",
    "/usr/local/include",
    "/opt/homebrew/opt/openblas/include",
    "/usr/local/opt/openblas/include",
]
for d in INCLUDE_DIRS_TO_SEARCH:
    if os.path.isdir(d):
        candidates = sorted(glob(os.path.join(d, "*openblas*")))
        if len(candidates) > 0:
            print(f"candidates = {candidates}")
            INCLUDE_DIRS.append(d)

LIBRARY_DIRS_TO_SEARCH = [
    "/usr/lib64",
    "/usr/local/lib64",
    "/opt/homebrew/opt/openblas/lib",
    "/usr/local/opt/openblas/lib",
]
for d in LIBRARY_DIRS_TO_SEARCH:
    if os.path.isdir(d):
        candidates = sorted(glob(os.path.join(d, "*openblas*")))
        if len(candidates) > 0:
            print(f"candidates = {candidates}")
            LIBRARY_DIRS.append(d)

CONDA_PREFIX = os.environ.get("CONDA_PREFIX")
if CONDA_PREFIX is not None:
    INCLUDE_DIRS.append(os.path.join(CONDA_PREFIX, "include"))
    LIBRARY_DIRS.append(os.path.join(CONDA_PREFIX, "lib"))

# Windows-conditional behavior
kwargs = {}
if os.name == "nt":
    # windows-2022 GitHub Actions image
    # include_dir = "C:\\Miniconda\\Library\\include\\openblas"
    include_dir = "C:\\Miniconda\\envs\\buildenv\\Library\\include\\openblas"
    library_dir = "C:\\Miniconda\\envs\\buildenv\\Library\\lib"
    bin_dir = "C:\\Miniconda\\envs\\buildenv\\Library\\bin"
    if os.path.isdir(include_dir) and os.path.isdir(library_dir):
        print("\nWINDOWS-2022 IMAGE DETECTED\n")
        INCLUDE_DIRS.append(include_dir)
        LIBRARY_DIRS.append(bin_dir)
        LIBRARY_DIRS.append(library_dir)
    elif CONDA_PREFIX is not None:
        include_dir = os.path.join(CONDA_PREFIX, "Library", "include", "openblas")
        if os.path.isdir(include_dir):
            INCLUDE_DIRS.append(include_dir)
            LIBRARY_DIRS.append(os.path.join(CONDA_PREFIX, "Library", "bin"))
            LIBRARY_DIRS.append(os.path.join(CONDA_PREFIX, "Library", "lib"))
else:
    kwargs["runtime_library_dirs"] = LIBRARY_DIRS


print(f"INCLUDE_DIRS = {INCLUDE_DIRS}")
print(f"LIBRARY_DIRS = {LIBRARY_DIRS}")

ext_modules = [
    Pybind11Extension(
        "_sargasso",
        SRC_PATHS,
        include_dirs=INCLUDE_DIRS,
        libraries=["openblas"],
        library_dirs=LIBRARY_DIRS,
        cxx_std=14,
        **kwargs,
    )
]

setuptools.setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
