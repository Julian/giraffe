from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
      name="giraffe",
      version="0.1",
      package_dir={"giraffe" : ""},
      packages=["giraffe"],
      cmdclass = {'build_ext': build_ext},
      ext_modules = [
                     Extension("graph", ["giraffe/graph.pyx"]),
                     Extension("graph_mixin", ["giraffe/graph_mixin.pyx"]),
                    ]
)
