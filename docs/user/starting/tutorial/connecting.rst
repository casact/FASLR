Connecting to the Database
==========================

When starting FASLR for the first time, you will see the :doc:`Main Window <../../interface/main>`. The Main Window has three sections - the Main Menu, the :doc:`Project Tree <../../interface/project>`, and the :doc:`Analysis Pane <../../interface/analysis>`. At first, the Project Tree and Analysis Pane will be blank. Before you create your first project, you will first need to connect to a :doc:`database <../../schema/index>`. The database is what keeps track of all the project metadata, and stores the associated loss and premium data.

.. image:: https://faslr.com/media/faslr_blank.png

To create a new database, navigate to **Main Menu -> File -> Connection**. You will see a dialog box asking whether you want to connect to an existing database, or create a new database. Select Create new database and then click **OK**. This will create a SQLite database where you can store your projects.

.. image:: https://faslr.com/media/faslr_connect.png

==================================
Automatically connect upon startup
==================================

By default, FASLR will not connect to this database upon startup. To avoid having to connect to it every time you run the program, you may opt to have FASLR establish the connection automatically. To do this, navigate to **Main Menu -> Settings -> Startup -> Add Connection**. This will open a dialog box asking you to select the SQLite file that you want to automatically connect to. Click OK to confirm, and FASLR will now connect to this database every time you start it.

.. image:: https://faslr.com/media/faslr_autoconnect.png

To cancel this association, click Reset Connection.