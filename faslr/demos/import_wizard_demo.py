import sys

from faslr.data import DataImportWizard

from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

wizard = DataImportWizard()
wizard.setWindowTitle("Import Wizard")

wizard.show()

app.exec()
