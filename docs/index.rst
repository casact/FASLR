:html_theme.sidebar_secondary.remove:

FASLR: Free Actuarial System for Loss Reserving
================================================

FASLR (fæzlɹ̩) is a Qt-based frontend for open-source loss reserving packages. Current plans are to support the `Chainladder <https://github.com/casact/chainladder-python/>`_ package.

FASLR will assist in the proper governance of periodic reserve reviews. In addition to being a GUI in which actuarial analyses can be done, it will also serve as a portal through which current and past analyses can be managed. Each reserve analysis will have metadata that indicates its status (in progress, review needed, signed-off), and by storing past analyses, FASLR will make it easy to compare quarter-by-quarter reviews without having to awkwardly navigate company shared folders and spreadsheets.

The actuarial methods and example data used in this project are derived from publicly available papers and data sources. The GUI is developed in Python using the open-source PyQt6 package. The `source code <https://github.com/casact/FASLR>`_ is available on the `CAS GitHub page <https://github.com/casact>`_.

.. image:: https://faslr.com/media/basic_ui_09082021.png

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Sections:

   user/index
   contributing/index
   api/index
   gallery/index