import csv
import io

from PyQt5.QtCore import (
    QAbstractTableModel,
    QEvent,
    Qt,
    QSize,
    QVariant
)

from PyQt5.QtGui import (
    QColor,
    QKeySequence
)

from PyQt5.QtWidgets import (
    QAbstractButton,
    QAction,
    QApplication,
    qApp,
    QLabel,
    QMenu,
    QStyle,
    QStylePainter,
    QStyleOptionHeader,
    QTableView,
    QVBoxLayout
)


class TriangleModel(QAbstractTableModel):

    def __init__(self, data):
        super(TriangleModel, self).__init__()
        self._data = data

        self.n_rows = self.rowCount()
        self.n_columns = self.columnCount()

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if str(value) == "nan":
                display_value = ""
            else:
                display_value = "{0:,.0f}".format(value)
                display_value = str(display_value)
            self.setData(self.index(index.row(), index.column()), QVariant(Qt.AlignRight),
                         Qt.TextAlignmentRole)

            return display_value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        if role == Qt.BackgroundRole and (index.column() >= self.n_rows - index.row()):
            return QColor(238, 237, 238)

    def rowCount(self, parent=None, *args, **kwargs):
        return self._data.shape[0]

    def columnCount(self, parent=None, *args, **kwargs):
        return self._data.shape[1]

    def headerData(self, p_int, qt_orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if qt_orientation == Qt.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Vertical:
                return str(self._data.index[p_int])


class TriangleView(QTableView):
    def __init__(self):
        super().__init__()

        self.copy_action = QAction("&Copy", self)
        self.copy_action.setShortcut(QKeySequence("Ctrl+c"))
        self.copy_action.setStatusTip("Copy selection to clipboard.")
        # noinspection PyUnresolvedReferences
        self.copy_action.triggered.connect(self.copy_selection)

        self.installEventFilter(self)

        btn = self.findChild(QAbstractButton)
        btn.installEventFilter(self)
        btn_label = QLabel("AY")
        btn_label.setAlignment(Qt.AlignCenter)
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(btn_label)
        btn.setLayout(btn_layout)
        opt = QStyleOptionHeader()

        self.setStyleSheet(
            """
            QTableCornerButton::section{
                border-width: 1px; 
                border-style: solid; 
                border-color:none darkgrey darkgrey none;
            }
            """
        )

        s = QSize(btn.style().sizeFromContents(
            QStyle.CT_HeaderSection, opt, QSize(), btn).
                  expandedTo(QApplication.globalStrut()))

        if s.isValid():
            self.verticalHeader().setMinimumWidth(s.width())

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Paint or not isinstance(
                obj, QAbstractButton):
            return False

        # Paint by hand (borrowed from QTableCornerButton)
        opt = QStyleOptionHeader()
        opt.initFrom(obj)
        style_state = QStyle.State_None
        if obj.isEnabled():
            style_state |= QStyle.State_Enabled
        if obj.isActiveWindow():
            style_state |= QStyle.State_Active
        if obj.isDown():
            style_state |= QStyle.State_Sunken
        opt.state = style_state
        opt.rect = obj.rect()
        # This line is the only difference to QTableCornerButton
        opt.text = obj.text()
        opt.position = QStyleOptionHeader.OnlyOneSection
        painter = QStylePainter(obj)
        painter.drawControl(QStyle.CE_Header, opt)

        return True

    def contextMenuEvent(self, event):
        """
        When right-clicking a cell, activate context menu.

        :param: event
        :return:
        """
        menu = QMenu()
        menu.addAction(self.copy_action)
        menu.exec(event.globalPos())

    def copy_selection(self):
        """Method to copy selected values to clipboard, so they can be pasted elsewhere, like Excel."""
        selection = self.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            qApp.clipboard().setText(stream.getvalue())
        return
