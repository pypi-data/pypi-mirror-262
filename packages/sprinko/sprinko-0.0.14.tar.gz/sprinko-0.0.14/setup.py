from setuptools import setup, find_packages

def get_version():
    with open("sprinko/core/__init__.py", "r") as f:
        content = f.readlines()

    for line in content:
        if "__version__ = " in line:
            version = line.split(" = ")[1].replace("\n", "")
            version = version.strip('"')
            break
    else:
        raise ValueError("version not found in __init__.py")

    return version
setup(
    name='sprinko',
    version=get_version(),
    packages=["sprinko", "sprinko.core"],
    author='ZackaryW',
    install_requires=[
        'click',
        'keyring',
        'masscode-driver',
        'keyrings.cryptfile',
    ],
    entry_points={
        'console_scripts': [
            'sprinko=sprinko.cli:cli',
        ],
    },
)