from setuptools import setup, find_packages

setup(
    name='wilder',
    version='0.1',
    packages=find_packages(),
    url = "https://github.com/MichaelTirat/wilder",
    description="Projet des compétences acquises à la Wild Code School et des mon travail autodidacte...",
    readme = "README.md",
    author='Michaël Tirat',
    author_email='michaeltirat@gmail.com',
    python_requires = ">= 3.10.9",
    install_requires=[
        'pandas >= 1.5.3'
    ],
    classifiers=[
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    py_modules=['wilder'],
)
