# Architecture

This file describes the overall directory structure of the FASLR repo and is intended to help those wishing to contribute or to simply learn about the project to navigate its contents.

# Overview

# FASLR Core

The [faslr](https://github.com/casact/FASLR/tree/main/faslr) folder contains the application's core libraries. The main application is located in main.py and can be activated by running this program.

# Templates

The [templates](https://github.com/casact/FASLR/tree/main/faslr/templates) directory contains files that are used as templates. These files are intended to be copied and used as user-specfic implementations. For example, [config-template.ini](https://github.com/casact/FASLR/blob/main/faslr/templates/config_template.ini) is the tempalte for the configuration file. This file is copied upon first use and contains settings unique to the user.

# Data Samples

The data samples used in testing FASLR during its development include those form the Chainladder package as well as from papers such as Friedland's landmark paper on basic reserving techniques. Sources that have been converted into csv files are located in the [samples](https://github.com/casact/FASLR/tree/main/faslr/samples) directory.