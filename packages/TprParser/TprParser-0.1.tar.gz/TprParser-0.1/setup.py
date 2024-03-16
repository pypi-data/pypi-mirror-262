from setuptools import setup, Extension
import numpy

module = Extension(
    name='TprParser',  # module name
    include_dirs=[numpy.get_include()], # need numpy
    language='C++',
    extra_compile_args=['-std:c++17'], # C++ standard
    define_macros=[('_CRT_SECURE_NO_WARNINGS', 1)], # for MSVC
    sources=['Py_Module.cpp', 'Reader.cpp'], # source code path
)
setup(
    name='TprParser',
    version='0.1',
    description='A reader of gromacs tpr file', 
    author='Yujie Liu',
    author_email='liuyujie714@hnu.edu.cn',
    python_requires='>=3.8',
    ext_modules=[module]
)
