from setuptools import setup, find_packages
import io
from os import path

# --- get version ---
version = "unknown"
with open("gymnasium_snake_game/version.py") as f:
    line = f.read().strip()
    version = line.replace("VERSION = ", "").replace("'", '')
# --- /get version ---

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gymnasium_snake_game',
    version=version,
    description='Snake game for Farama Gymnasium',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lychanl/Gymnasium_Snake_Game',
    author='Jakub Łyskawa',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',

        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Games/Entertainment :: Arcade',

        'Programming Language :: Python :: 3.10',
    ],
    platforms=['any'],
    keywords='ai, rl, snake',
    packages=find_packages(),
    python_requires='>=3.0',
    install_requires=['pygame>=2.1.0', 'numpy>=1.21', 'gymnasium>=0.29'],
)
