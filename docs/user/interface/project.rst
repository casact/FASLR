Project Tree
============

The project tree is the pane located on the left side of the :doc:`Main Window <main>`. It contains the lists of projects that have been saved to the underlying database, organized hierarchically by geographic region.


.. image:: https://faslr.com/meda/project_tree.png

The current hierarchy is:

Country -> State -> Line of Business (LOB)

This means that each country may contain multiple states, and each state can have multiple lines of business. There are `plans in the future <https://github.com/casact/FASLR/discussions/67>`_ to allow users to implement a custom hierarchy if the current one does not fit their needs.

Each node in the tree is uniquely identified by a UUID string. This makes it easier to unambiguously refer to a project so that they may be shared with colleagues.
