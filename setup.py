import re
import setuptools

# from faslr.constants import BUILD_VERSION

def get_property(
        prop: str,
        project: str
) -> str:

    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(project + '/__init__.py').read())

    return result.group(1)

project_name = 'faslr'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=project_name,
    version=get_property('__version__', project_name),
    author="Gene Dan",
    author_email="genedan@gmail.com",
    description="Free Actuarial System for Loss Reserving",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genedan/FASLR",
    project_urls={
        "Documentation": "https://genedan.com/faslr/docs"
    },
    install_requires=[
        'bs4',
        'chainladder',
        'GitPython',
        'matplotlib',
        'numpy',
        'pandas',
        'pydata-sphinx-theme',
        'pytest',
        'pytest-cov',
        'PyQt6',
        'sphinx_design',
        'sqlalchemy'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.10.0',
)