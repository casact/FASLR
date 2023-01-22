from __future__ import annotations
# from random import sample
import chainladder as cl
import matplotlib
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.base_classes import (
    FComboBox,
    FDoubleSpinBox,
    FHContainer,
    FSpinBox
)

from faslr.constants import (
    ICONS_PATH
)

from functools import partial

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg
)

from matplotlib.figure import Figure

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtGui import (
    QIcon
)

from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QToolButton,
    QWidget,
    QStackedWidget,
    QStatusBar,
    QTabWidget,
    QVBoxLayout
)

from typing import (
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from chainladder import Triangle

matplotlib.use('Qt5Agg')

curve_alias = {
    'Exponential': 'exponential',
    'Inverse Power': 'inverse_power'
}


class TailPane(QWidget):
    def __init__(
            self,
            triangle: Triangle = None
    ):
        super().__init__()

        self.triangle = triangle
        self.toggled_chart = 'curve_btn'

        # list to hold each tail candidate
        self.tail_candidates = []
        self.setWindowTitle("Tail Analysis")

        self.max_tab_idx = 1

        self.sc = MplCanvas(
            self,
            dpi=100
        )

        # main layout
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        main_container = QWidget()
        main_container.setLayout(hlayout)
        # hlayout.setContentsMargins(0,0,0,0)
        main_container.setContentsMargins(
            0,
            0,
            0,
            0
        )
        # vlayout.setContentsMargins(0,0,0,0)
        vlayout.addWidget(main_container)

        # canvas layout to enable margin adjustments
        canvas_layout = QVBoxLayout()
        canvas_container = QWidget()
        canvas_container.setLayout(canvas_layout)

        # layout to toggle between charts
        ly_graph_toggle = QVBoxLayout()
        ly_graph_toggle.setAlignment(Qt.AlignmentFlag.AlignTop)
        graph_toggle_btns = QWidget()
        graph_toggle_btns.setLayout(ly_graph_toggle)

        curve_btn = QPushButton('')
        curve_btn.setIcon(QIcon(ICONS_PATH + 'graph-down.svg'))
        curve_btn.setToolTip('Development factor comparison')
        curve_btn.clicked.connect(partial(self.toggle_chart, 'curve_btn')) # noqa

        tail_comps_btn = QPushButton('')
        tail_comps_btn.setIcon(QIcon(ICONS_PATH + 'bar-chart-2.svg'))
        tail_comps_btn.setToolTip('Tail factor comparison')
        tail_comps_btn.clicked.connect(partial(self.toggle_chart, 'tail_comps_btn')) # noqa

        extrap_btn = QPushButton('')
        extrap_btn.setIcon(QIcon(ICONS_PATH + 'noun-curve-graph-1476204.svg'))
        extrap_btn.setToolTip('Extrapolation')
        extrap_btn.clicked.connect(partial(self.toggle_chart, 'extrap_btn')) # noqa

        reg_btn = QPushButton('')
        reg_btn.setIcon(QIcon(ICONS_PATH + 'noun-scatter-plot-4489619.svg'))
        reg_btn.setToolTip('Fit period comparison')
        reg_btn.clicked.connect(partial(self.toggle_chart, 'reg_btn')) # noqa

        ly_graph_toggle.addWidget(curve_btn)
        ly_graph_toggle.addWidget(tail_comps_btn)
        ly_graph_toggle.addWidget(extrap_btn)
        ly_graph_toggle.addWidget(reg_btn)

        ly_graph_toggle.setContentsMargins(
            0,
            40,
            0,
            0
        )

        # Tabs to hold each tail candidate
        self.config_tabs = QTabWidget()
        add_tab_btn = QToolButton()
        add_tab_btn.setText('+')
        add_tab_btn.setFixedHeight(22)
        add_tab_btn.setFixedWidth(22)
        add_tab_btn.setToolTip('Add tail candidate')
        remove_tab_btn = QToolButton()
        remove_tab_btn.setText('-')
        remove_tab_btn.setToolTip('Remove tail candidate')
        remove_tab_btn.setFixedWidth(add_tab_btn.width())
        remove_tab_btn.setFixedHeight(add_tab_btn.height())
        ly_tab_btn = QHBoxLayout()
        ly_tab_btn.setContentsMargins(
            0,
            0,
            0,
            2
        )
        ly_tab_btn.setSpacing(2)
        tab_btn_container = QWidget()
        tab_btn_container.setContentsMargins(
            0,
            0,
            0,
            0
        )
        tab_btn_container.setLayout(ly_tab_btn)
        ly_tab_btn.addWidget(add_tab_btn)
        ly_tab_btn.addWidget(remove_tab_btn)
        # add_tab_btn.setFixedWidth(30)
        self.config_tabs.setCornerWidget(
            tab_btn_container,
            Qt.Corner.TopRightCorner
        )

        add_tab_btn.pressed.connect(self.add_tab) # noqa
        remove_tab_btn.pressed.connect(self.remove_tab) # noqa

        tail_config = TailConfig(parent=self)
        self.tail_candidates.append(tail_config)

        self.config_tabs.addTab(tail_config, "Tail 1")

        hlayout.addWidget(
            self.config_tabs,
            stretch=0
        )

        canvas_layout.addWidget(self.sc)

        # The goal for setting these margins is to align the chart position with the group boxes on the left
        canvas_layout.setContentsMargins(
            11,
            26,
            11,
            0
        )

        hlayout.addWidget(
            canvas_container,
            stretch=1
        )

        hlayout.addWidget(
            graph_toggle_btns
        )

        self.setLayout(vlayout)

        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.button_layout = self.ok_btn
        self.button_box = QDialogButtonBox(self.button_layout)
        self.button_box.accepted.connect(self.close) # noqa

        vlayout.addWidget(self.button_box)
        self.update_plot()

    def add_tab(self) -> None:
        print(self.config_tabs.currentIndex())
        new_tab = TailConfig(parent=self)

        self.tail_candidates.append(new_tab)

        tab_count = self.config_tabs.count()

        self.config_tabs.addTab(
            new_tab,
            'Tail ' + str(self.max_tab_idx + 1)
        )

        self.max_tab_idx += 1

        self.config_tabs.setCurrentIndex(tab_count)

        self.update_plot()

    def remove_tab(self) -> None:

        # do nothing if there is only 1 tab
        if self.config_tabs.count() == 1:
            return

        idx = self.config_tabs.currentIndex()
        self.tail_candidates.remove(self.config_tabs.currentWidget())

        self.config_tabs.removeTab(idx)

        self.update_plot()

    def update_plot(self) -> None:

        self.sc.axes.cla()

        if self.toggled_chart == 'curve_btn':

            self.sc.axes.cla()
            # self.sc.axes.get_legend().remove()
            x = []
            y = []

            for config in self.tail_candidates:

                if config.constant_btn.isChecked():
                    tail_constant = config.constant_config.sb_tail_constant.spin_box.value()
                    decay = config.constant_config.sb_decay.spin_box.value()
                    attach = config.constant_config.sb_attach.spin_box.value()
                    projection = config.constant_config.sb_projection.spin_box.value()

                    tc = cl.TailConstant(
                        tail=tail_constant,
                        decay=decay,
                        attachment_age=attach,
                        projection_period=projection
                    ).fit_transform(self.triangle)

                    x.append(list(tc.cdf_.to_frame(origin_as_datetime=True)))
                    y.append(tc.cdf_.iloc[:len(x), 0].values.flatten().tolist())

                else:  # config.curve_btn.isChecked():
                    curve = curve_alias[config.curve_config.curve_type.combo_box.currentText()]
                    fit_from = config.curve_config.fit_from.spin_box.value()
                    fit_to = config.curve_config.fit_to.spin_box.value()

                    tc = cl.TailCurve(
                        curve=curve,
                        fit_period=(
                            fit_from,
                            fit_to
                        )
                    ).fit_transform(self.triangle)

            for i in range(len(x)):

                self.sc.axes.plot(
                    x[i],
                    y[i],
                    label=self.config_tabs.tabText(i)
                )

            self.sc.axes.legend()

            self.sc.axes.xaxis.set_major_locator(plt.MaxNLocator(6))

            self.sc.axes.spines['bottom'].set_color('0')

            self.sc.axes.set_title("Selected Cumulative Development Factor")

            self.sc.draw()
        elif self.toggled_chart == 'tail_comps_btn':

            clrd = cl.load_sample('clrd').groupby('LOB').sum()['CumPaidLoss']
            cdf_ip = cl.TailCurve(curve='inverse_power').fit(clrd).tail_ # noqa
            cdf_xp = cl.TailCurve(curve='exponential').fit(clrd).tail_ # noqa

            labels = list(cdf_ip.rename("Inverse Power").index)
            x = np.arange(len(labels))
            y1 = list(cdf_ip.rename("Inverse Power"))
            y2 = list(cdf_xp.rename("Exponential"))

            width = .4
            self.sc.axes.cla()

            rects1 = self.sc.axes.bar(x=x - width / 2, width=width, height=y1, label='Inverse Power')
            rects2 = self.sc.axes.bar(x=x + width / 2, width=width, height=y2, color='lightcoral', label='Exponential')
            self.sc.axes.set_ylabel('Tail Factor')
            self.sc.axes.set_title('Curve Fit Comparison')
            self.sc.axes.set_xticks(x, labels)
            self.sc.axes.legend()

            self.sc.draw()
        elif self.toggled_chart == 'extrap_btn':

            tri = cl.load_sample('clrd').groupby('LOB').sum().loc['medmal', 'CumPaidLoss']

            # Create a fuction to grab the scalar tail value.
            def scoring(model):
                """ Scoring functions must return a scalar """
                return model.tail_.iloc[0, 0]

            # Create a grid of scenarios
            param_grid = dict(
                extrap_periods=list(range(1, 100, 6)),
                curve=['inverse_power', 'exponential'])

            # Fit Grid
            model = cl.GridSearch(cl.TailCurve(), param_grid=param_grid, scoring=scoring).fit(tri)

            # Plot results
            pvt = model.results_.pivot(columns='curve', index='extrap_periods', values='score')

            x = list(pvt.index)
            y1 = pvt['exponential']
            y2 = pvt['inverse_power']

            self.sc.axes.cla()

            self.sc.axes.plot(x, y1, label='Exponential')
            self.sc.axes.plot(x, y2, label='Inverse Power')
            self.sc.axes.set_title('Curve Fit Sensitivity to Extrapolation Period')
            self.sc.axes.set_ylabel('Tail factor')
            self.sc.axes.set_xlabel('Extrapolation Periods')
            self.sc.axes.legend()

            self.sc.draw()

        else:
            dev = cl.Development().fit_transform(cl.load_sample('quarterly')['paid'])
            fit_all = cl.TailCurve().fit(dev)
            exclude = cl.TailCurve(fit_period=(36, None)).fit(dev)

            obs = (dev.ldf_ - 1).T.iloc[:, 0]
            obs[obs < 0] = np.nan

            ax = np.log(obs).rename('Selected LDF')

            x = list(ax.index)
            y1 = list(np.log(obs).rename('Selected LDF'))

            y2 = list(pd.Series(
                np.arange(1, dev.ldf_.shape[-1] + 1) * exclude.slope_.sum().values + exclude.intercept_.sum().values,
                index=dev.ldf_.development,
                name=f'Ages after 36: {round(exclude.tail_.values[0, 0], 3)}'))

            y3 = list(pd.Series(
                np.arange(1, dev.ldf_.shape[-1] + 1) * fit_all.slope_.sum().values + fit_all.intercept_.sum().values,
                index=dev.ldf_.development,
                name=f'All Periods: {round(fit_all.tail_.values[0, 0], 3)}'))

            self.sc.axes.cla()

            self.sc.axes.scatter(x, y1)
            self.sc.axes.plot(x, y2, linestyle='--', label='Ages after 36: 1.002')
            self.sc.axes.plot(x, y3, linestyle='-.', color='darkorchid', label='All Periods: 1.001')
            self.sc.axes.set_xlabel('Development')
            self.sc.axes.set_title('Fit Period Affect on Tail Estimate')
            self.sc.axes.legend()

            self.sc.axes.xaxis.set_major_locator(plt.MaxNLocator(6))


            self.sc.draw()

    def toggle_chart(self, value) -> None:

        self.toggled_chart = value

        self.update_plot()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(
            self,
            parent: TailPane = None,
            width=5,
            height=4,
            dpi=100
    ):
        self.parent = parent

        fig = Figure(
            figsize=(
                width,
                height
            ),
            dpi=dpi,
            linewidth=1,
            edgecolor='#ababab'
        )

        self.axes = fig.add_subplot(111)

        super(MplCanvas, self).__init__(fig)


class ConstantConfig(QWidget):
    def __init__(
            self,
            parent: TailConfig = None
    ):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.sb_tail_constant = FDoubleSpinBox(
            label='Tail Constant: ',
            value=1.00,
            single_step=.01
        )

        self.sb_decay = FDoubleSpinBox(
            label='Decay: ',
            value=0.5,
            single_step=.01
        )

        self.sb_attach = FSpinBox(
            label='Attachment Age: ',
            value=120,
            single_step=1
        )

        self.sb_projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.layout.addWidget(self.sb_tail_constant)
        self.layout.addWidget(self.sb_decay)
        self.layout.addWidget(self.sb_attach)
        self.layout.addWidget(self.sb_projection)

        self.sb_tail_constant.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.sb_decay.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.sb_attach.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.sb_projection.spin_box.valueChanged.connect(parent.parent.update_plot)


class CurveConfig(QWidget):
    def __init__(
            self,
            parent: TailConfig = None
    ):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.curve_type = FComboBox(label="Curve Type:")
        self.curve_type.combo_box.addItems([
            "Inverse Power",
            "Exponential"
        ])

        fit_period = FHContainer()
        fit_period_label = QLabel("Fit Period: ")
        self.fit_from = FSpinBox(
            label="From: ",
            value=12,
            single_step=12
        )
        self.fit_to = FSpinBox(
            label="To: ",
            value=120,
            single_step=12
        )
        fit_period.layout.addWidget(fit_period_label)
        fit_period.layout.addWidget(self.fit_from)
        fit_period.layout.addWidget(self.fit_to)

        extrap_periods = FSpinBox(
            label="Extrapolation Periods: ",
            value=100,
            single_step=1
        )

        errors = FHContainer()
        errors_label = QLabel("Errors: ")
        errors_ignore = QRadioButton("Ignore")
        errors_raise = QRadioButton("Raise")
        errors_ignore.setChecked(True)

        errors.layout.addWidget(errors_label)
        errors.layout.addWidget(errors_ignore)
        errors.layout.addWidget(errors_raise)

        attachment_age = FSpinBox(
            label='Attachment Age: ',
            value=120,
            single_step=1
        )

        projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.curve_type.combo_box.setCurrentText("Exponential")

        layout.addWidget(self.curve_type)
        layout.addWidget(fit_period)
        layout.addWidget(extrap_periods)
        layout.addWidget(errors)
        layout.addWidget(attachment_age)
        layout.addWidget(projection)

        self.curve_type.combo_box.currentTextChanged.connect(parent.parent.update_plot)
        self.fit_from.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.fit_to.spin_box.valueChanged.connect(parent.parent.update_plot)


class ClarkConfig(QWidget):
    def __init__(
            self,
            parent: TailConfig = None
    ):
        super().__init__()

        self.parent = parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        growth = FComboBox(
            label="Growth: "
        )

        truncation_age = FSpinBox(
            label="Truncation Age: ",
            value=120,
            single_step=12
        )

        attachment_age = FSpinBox(
            label="Attachment Age: ",
            value=120,
            single_step=12
        )

        projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        growth.combo_box.addItems([
            'Loglogistic',
            'Weibull'
        ])

        layout.addWidget(growth)
        layout.addWidget(truncation_age)
        layout.addWidget(attachment_age)
        layout.addWidget(projection)


class BondyConfig(QWidget):
    def __init__(
            self,
            parent: TailConfig = None
    ):
        super().__init__()

        self.parent = parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        earliest_age = FSpinBox(
            label="Earliest Age: ",
            value=120,
            single_step=12
        )

        attachment_age = FSpinBox(
            label="Attachment Age: ",
            value=120,
            single_step=12
        )

        projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        layout.addWidget(earliest_age)
        layout.addWidget(attachment_age)
        layout.addWidget(projection)


class TailConfig(QWidget):
    def __init__(
            self,
            parent: TailPane = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.gb_tail_type = QGroupBox("Tail Type")

        self.ly_tail_type = QHBoxLayout()

        self.bg_tail_type = QButtonGroup()
        self.constant_btn = QRadioButton('Constant')
        self.curve_btn = QRadioButton('Curve')
        self.bondy_btn = QRadioButton('Bondy')
        self.clark_btn = QRadioButton('Clark')

        buttons = [
            self.constant_btn,
            self.curve_btn,
            self.bondy_btn,
            self.clark_btn
        ]

        for button in buttons:
            self.bg_tail_type.addButton(button)
            self.ly_tail_type.addWidget(button)

        self.gb_tail_type.setLayout(self.ly_tail_type)

        self.cb_mark_selected = QCheckBox('Mark as selected')

        self.gb_tail_params = QGroupBox("Tail Parameters")
        self.ly_tail_params = QVBoxLayout()
        self.gb_tail_params.setLayout(self.ly_tail_params)

        self.params_config = QStackedWidget()

        self.constant_config = ConstantConfig(parent=self)
        self.curve_config = CurveConfig(parent=self)
        self.bondy_config = BondyConfig(parent=self)
        self.clark_config = ClarkConfig(parent=self)

        configs = [
            self.constant_config,
            self.curve_config,
            self.bondy_config,
            self.clark_config
        ]

        for config in configs:
            self.params_config.addWidget(config)

        self.ly_tail_params.addWidget(self.params_config)
        # self.gb_tail_params.setFixedWidth(config_width)

        self.layout.addWidget(self.gb_tail_type)
        self.layout.addWidget(self.gb_tail_params)
        self.layout.addWidget(self.cb_mark_selected)

        self.constant_btn.setChecked(True)
        self.bg_tail_type.buttonToggled.connect(self.set_config)  # noqa

    def set_config(self):

        if self.constant_btn.isChecked():
            self.params_config.setCurrentIndex(0)
        elif self.curve_btn.isChecked():
            self.params_config.setCurrentIndex(1)
        elif self.bondy_btn.isChecked():
            self.params_config.setCurrentIndex(2)
        elif self.clark_btn.isChecked():
            self.params_config.setCurrentIndex(3)

        self.parent.update_plot()


class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()
