# About
The purpose of this library is to provide a logger for my other projects. It also
is acting as a learning process for publishing a python module.

# TODO:
sort out the proper file / function printing

# Messages Package
This is a package that can be included in projects to output messages

Example logging REPO: https://github.com/srtamrakar/python-logger/tree/master


# Installation Process:
    1. Write the module
        - Follow this tutorial: https://packaging.python.org/en/latest/tutorials/packaging-projects/
    2. Build module
        - python3 -m pip install --upgrade build
        - python3 -m build
    3. Upload module to pypi to be installed: https://packaging.python.org/en/latest/tutorials/packaging-projects/
        - python3 -m pip install --upgrade twine


# Repository structure
    .gitignore
    .venv
        bin
            activate...
            pip
            pip3
            pip3.11
            python
            python3
            python3.11
        include
            python3.11
                ...
        lib
            python3.11
                ...
        pyenv.cfg
    dist
        phootlogger-0.0.1-py3-none-any.whl
        phootlogger-0.0.1.tar.gz
    LICENSE
    pyproject.toml
    setup.py
    src
        phootlogger
            __init__.py
            __pycache__
            logger.py
        phootlogger.egg-info
        demo.py
    README.md
    requirements.txt
    tests



<pip install .>

installs:
    tar under the 'dist'
    creates .egg-info

Needed files:
    setup.py
    LICEANSE
    README


Layouts:
    flat-layouts:

    src-layout:



Questions:
    setup.cfg:
        

    setup.py:
        Instructions to build software. Maybe some configuration options like computing test coverage or unit tests or
        the install prefix.

    pyproject.toml:
        Specifies the project's metadata.
        Used to replace .cfg, but formats everything in TOML. ( Tom's Obvious, Minimal Language: https://en.wikipedia.org/wiki/TOML )
        You can put "Abstract Dependancies" here, but not pinned dependencies. Pinned ones belong in the requirements.txt

    requirements.txt:
        Not the same thing as setup.cfg. Needed for a different reason. This is typically used for deploymnet with
        version pinned dependencies. The reason is so you don't get the latest and greatest, and only get the version
        you know you have explicitley tested.
