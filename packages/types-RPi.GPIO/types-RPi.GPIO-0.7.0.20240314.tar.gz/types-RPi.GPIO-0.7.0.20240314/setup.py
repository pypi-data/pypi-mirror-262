from setuptools import setup

name = "types-RPi.GPIO"
description = "Typing stubs for RPi.GPIO"
long_description = '''
## Typing stubs for RPi.GPIO

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`RPi.GPIO`](https://sourceforge.net/p/raspberry-gpio-python/code/) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`RPi.GPIO`.

This version of `types-RPi.GPIO` aims to provide accurate annotations
for `RPi.GPIO==0.7.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/RPi.GPIO. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `a1bfd65e9fa92e1bb61a475c7622ba0376d936d5` and was tested
with mypy 1.9.0, pyright 1.1.350, and
pytype 2024.2.27.
'''.lstrip()

setup(name=name,
      version="0.7.0.20240314",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/RPi.GPIO.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['RPi-stubs'],
      package_data={'RPi-stubs': ['GPIO/__init__.pyi', '__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
