import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyBitgetApi",
    version="0.1.1",
    description="Un exemple de package Python dans un sous-dossier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': '.'},
    packages=setuptools.find_packages(where='.'), 
    install_requires=[
        "logger",
        "requests",
        "websocket-client"
    ],
)
