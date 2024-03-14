from Cython.Distutils import build_ext
from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension

ext_modules = [
    Extension(
        name="ngu",
        sources=[
            "ngu.pyx", 
        ],
        include_dirs=["./ngu"],
        language="c++",
    ), 
]
setup(
    name = "ngu",
    version = "1.0.7",
    description = "",
    long_description = "",
    author = "",
    author_email = "",
    url = "",
    ext_modules = ext_modules,
    setup_requires=["cython"],
    cmdclass = { "build_ext": build_ext }
)
