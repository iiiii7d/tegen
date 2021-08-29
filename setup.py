from setuptools import setup
import tegen

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'tegen',
  packages = ['tegen'],
  version = tegen.__version__+"",
  license ='gpl-3.0',
  description = 'Terminal game engine for Python',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = '7d',
  author_email = 'i.third.7d@protonmail.com',
  url = 'https://github.com/iiiii7d/tegen',
  download_url = f'https://github.com/iiiii7d/tegen/archive/refs/tags/v{tegen.__version__}.tar.gz',
  keywords = ['tegen', 'terminal', 'game', 'engine', 'terminal game engine', 'game development'],
  python_requires='>=3.6',
  package_data={
    'tegen': ['examples/*'],
  },
  install_requires=[
    "blessed",
    "wcwidth",
    "pillow"
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Games/Entertainment",
  ],
)

#commands for upload in case i forget
#python setup.py sdist
#python setup.py bdist_wheel
#twine upload dist/*