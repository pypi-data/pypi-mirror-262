from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='gurulearn',
    version='1.0.3',
    description='library for linear_regression and gvgg16 model generation',
    author='Guru Dharsan T',
    author_email='gurudharsan123@gmail.com',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'scipy',
        'matplotlib',
        'tensorflow',
        'Keras',
        'pandas',
        'numpy',
        'plotly',
        'scikit-learn',
    ],
)
