import setuptools

from faslr.constants import BUILD_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faslr",
    version=BUILD_VERSION,
    author="Gene Dan",
    author_email="genedan@gmail.com",
    description="Free Actuarial System for Loss Reserving",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genedan/FASLR",
    project_urls={
        "Documentation": "https://genedan.com/faslr/docs"
    },
    install_requires=['chainladder', 'PyQt5'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6.0',
)