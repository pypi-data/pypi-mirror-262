from setuptools import setup, find_packages


setup(
    name='awesome-latex-maker',
    version='0.0.2',
    description='Awesome LaTeX Maker',
    long_description='Awesome LaTeX Maker',
    long_description_content_type='text/plain',
    author='Georgii Angeni',
    package_dir={'': 'latex_maker'},
    packages=find_packages(where='latex_maker'),
    python_requires='>=3.11, <4',
    install_requires=['pdflatex']
)
