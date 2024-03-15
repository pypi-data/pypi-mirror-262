from setuptools import setup, find_packages


setup(
    name='awesome-latex-maker',
    version='0.0.3',
    description='Awesome LaTeX Maker',
    long_description='Awesome LaTeX Maker',
    long_description_content_type='text/plain',
    author='Georgii Angeni',
    packages=find_packages(),
    python_requires='>=3.11, <4',
    install_requires=['pdflatex']
)
