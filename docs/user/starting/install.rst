Setup and Installation
=======================

FASLR is in the early stages of development. As such, rapid implementation of features has been prioritized over the stability of the user experience. There are currently no binary executables available. People who are interested in seeing what FASLR can do as well as potential contributors will, for the time being, need to run FASLR from source.

=======================
Cloning the Repository
=======================

The first step in using FASLR is to clone the repository from the `CAS GitHub <https://github.com/casact/>`_. This can be done by opening a terminal, navigating to the directory where you want to keep the repo, and then running the command:

.. code-block:: shell

   git clone https://github.com/casact/faslr

========================
Installing Dependencies
========================

I recommend that you use a virtual environment to avoid package conflicts.

The Python package dependencies is located in the `requirements.txt <https://github.com/casact/FASLR/blob/main/requirements.txt>`_ file. These can be installed with the following command:

.. code-block:: shell

    pip install -r requirements.txt

==============
Running FASLR
==============

Once the packages have been installed, you can run FASLR by executing the `main.py <https://github.com/casact/FASLR/blob/main/faslr/main.py>`_ file in the `faslr directory <https://github.com/casact/FASLR/tree/main/faslr>`_:

.. code-block:: shell

   python -m faslr.main

Alternatively, if you have a virtual environment set up:

.. code-block:: shell

   source venv/bin/activate
   python -m faslr.main

===========
Demo files
===========

In addition to the main program, you can run test out individual widgets by running the files in the `demos <https://github.com/casact/FASLR/tree/main/faslr/demos>`_ folder.
