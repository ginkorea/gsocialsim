from setuptools import setup

try:
    from pybind11.setup_helpers import Pybind11Extension, build_ext
except Exception:
    Pybind11Extension = None
    build_ext = None

ext_modules = []
cmdclass = {}

if Pybind11Extension is not None:
    ext_modules = [
        Pybind11Extension(
            "gsocialsim.fast._fast_perception",
            ["python/src/gsocialsim/fast/perception.cpp"],
            cxx_std=17,
        )
    ]
    cmdclass = {"build_ext": build_ext}

setup(
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)
