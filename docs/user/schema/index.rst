Introduction
================

FASLR stores project metadata and data in a relational database. SQLite is the current database technology used for this purpose. While the ultimate vision is to eventually use enterprise-level databases (such as SQL Server), SQLite allows rapid changes to the underlying FASLR schema, makes FASLR easier to distribute, and eases the startup burden on the user.

Should the project become more serious, the plan is to adapt FASLR to more serious databases.

More detailed information can be found on the `SchemaSpy <https://faslr.com/db/>`_ page.

.. image:: https://faslr.com/media/schema.png
