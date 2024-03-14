from setuptools import setup, find_packages

setup(
    name='QuGIT_v2',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    author='Jose Manuel Montes Armenteros',
    author_email='jose.manuelmontes@hotmail.com',
    description='QuGIT is an open-sourced object-oriented Python library aimed at simulating multimode quantum gaussian states.\n QuGIT_v2 is focused in the computation of correlations between modes, primarily using the Logarithmic Negativity',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    license='BSD-3-Clause',
    # This package makes use of QuGIT: Quantum Gaussian Information Toolbox
    # developed by I. Brandão and D. Tandeitnik
    # For more info go to https://github.com/IgorBrandao42/Quantum-Gaussian-Information-Toolbox
)