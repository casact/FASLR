Importing Data
==============

In the project tree, double click on a project. This will open up the project data view pane in the Analysis Pane of the Main Window. This pane lists the data views associated with the project. If you have not yet uploaded data, this view will be blank.

.. image:: https://faslr.com/media/empty_data_view.png

To upload data, click on the **Upload** button in the upper right-hand corner of the project data views pane. This will activate an import wizard, which you can use to upload a CSV file.

.. image:: https://faslr.com/media/import_wizrd.png
   :width: 400px

To upload a CSV file, click the **Upload File** button. Right now, FASLR only accepts data that conform to the way the chainladder-python package accepts tabular data. For guidelines on how to format the source data, see chainladder `tutorial on triangles <https://chainladder-python.readthedocs.io/en/latest/tutorials/triangle-tutorial.html>`_.

.. image:: https://faslr.com/media/import_wizard_filled.png
   :width: 400px

Assuming you did that correctly, you should see the data views pane populated with an entry after you press the **OK** button.

.. image:: https://faslr.com/media/data_view_filled.png

To see the triangle contained in this view, double click the entry in the table, and a new tab will open up, displaying the triangle data:

.. image:: https://faslr.com/media/data_view_preview.png