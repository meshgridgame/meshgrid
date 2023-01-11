import setuptools

setuptools.setup(
    name = 'meshgrid',
    version = '0.0.2',
    author = 'Kyle Horn',
    author_email = 'meshgrid.game@gmail.com',
    description = 'A Jupyter Notebook based game engine for grid-based games',
    package_dir = {'': 'src'},
    install_requires = ['jupyter','numpy','ipycanvas'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)