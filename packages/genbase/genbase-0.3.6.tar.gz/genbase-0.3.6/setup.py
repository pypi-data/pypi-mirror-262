from distutils.util import convert_path
from os import path

import setuptools

main_ns = {}
with open(convert_path('genbase/_version.py')) as ver_file:
    exec(ver_file.read(), main_ns)  # nosec

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup( # type: ignore
    name = 'genbase',
    version = main_ns['__version__'],
    description = 'Generation base dependency',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Marcel Robeer',
    author_email = 'm.j.robeer@uu.nl',
    license = 'GNU LGPL v3',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    url = 'https://git.science.uu.nl/m.j.robeer/genbase',
    packages = setuptools.find_packages(), # type : ignore
    include_package_data = True,
    install_requires = [
        'instancelib>=0.4.4.1',
        'instancelib-onnx>=0.1.3',
        'onnxruntime; python_version < "3.10"',
        'onnxruntime>=1.12.0; python_version >= "3.10"',
        'matplotlib>=3.5.0',
        'numpy>=1.19.5',
        'python-i18n>=0.3.9',
        'srsly>=2.4.2',
        'requests',
        'ipython>=7.30.1',
        'lazy-load>=0.8.2',
    ],
    python_requires = '>=3.8'
)
