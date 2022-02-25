# FASLR
Free Actuarial System for Loss Reserving

FASLR (fæzlɹ̩) is a Qt-based frontend for open-source loss reserving packages. Current plans are to support the [Chainladder](https://github.com/casact/chainladder-python) package.

The actuarial methods and example data used in this project are derived from publicly available papers and data sources. The GUI is developed in Python using the open-source PyQt5 package.

Since PyQt6 has been released, I'm considering upgrading the project to PyQt6. A branch has been created for this purpose a thread in the discussions section has been started.

## Project Governance

FASLR will assist in the proper governance of periodic reserve reviews. In addition to being a GUI in which actuarial analyses can be done, it will also serve as a portal through which current and past analyses can be managed. Each reserve analysis will have metadata that indicates its status (in progress, review needed, signed-off), and by storing past analyses, FASLR will make it easy to compare quarter-by-quarter reviews without having to awkwardly navigate company shared folders.

## Basic Interface

FASLR will have a simple layout. The collapsible side pane will contain a navigable tree consisting of past reserve analyses, organized by jurisdiction, LOB, and unit of time.

The analysis pane is where the user will be able to conduct a reserve analysis. This will be the area where the actuary can view triangles, select and perform actuarial methods, and view graphs. The user will also be able to toggle between an analysis view (doing the work) and project metadata (project status, peer review, sign off).

![basic-interface-filled](docs/_static/basic_ui_09082021.png)
![basic-interface-filled](docs/_static/dev_demo.gif)
![basic-interface](docs/_static/basic_interface.png)

## Department Integration

FASLR will support departments with multiple users, who will have the ability to check out and lock analyses as they are being used. Data will be stored on a database, although the ones that will be supported have yet to be determined. Lightweight deployments for single-users or personal use will use a SQLite data store.

![client-server-model](docs/_static/client_server.png)

## Contributing

You can evaluate the working version of FASLR by executing the [main.py](https://github.com/casact/FASLR/blob/main/faslr/main.py) program in the [faslr](https://github.com/casact/FASLR/tree/main/faslr) directory.

To learn more about the current structure of the repository, read [ARCHITECTURE.md](https://github.com/casact/FASLR/blob/main/ARCHITECTURE.md).

## Supported Operating Systems

FASLR is currently supported on Linux. However, I recognize that almost all actuarial work is done on Windows machines, so there may be plans in the future to make things compatible with that operating system. 