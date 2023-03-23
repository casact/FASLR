from __future__ import annotations
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

from faslr.common import (
    AddRemoveButtonWidget
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
    QWidget,
    QStackedWidget,
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

clark_alias = {
    'Loglogistic': 'loglogistic',
    'Weibull': 'weibull'
}

fit_errors = {
    'Ignore': 'ignore',
    'Raise': 'raise'
}


class TailPane(QWidget):
    def __init__(
            self,
            triangle: Triangle = None
    ):
        """
        Dialog box for conducting tail analyses. Holds configuration sub widgets for various tail-factor models
        (Constant, Curve, Clark, Bondy) as well as a canvas for plotting diagnostic charts.

        :param triangle:
        """
        super().__init__()

        self.triangle = triangle

        # Holds the currently toggled chart
        self.toggled_chart = 'curve_btn'

        # list to hold each tail candidate
        self.tail_candidates = []
        self.setWindowTitle("Tail Analysis")

        # number of tabs that have been created, used to create default names for the candidate tabs
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
        main_container.setContentsMargins(
            0,
            0,
            0,
            0
        )
        vlayout.addWidget(main_container)

        # canvas layout to enable margin adjustments
        canvas_layout = QVBoxLayout()
        canvas_container = QWidget()
        canvas_container.setLayout(canvas_layout)

        # layout to toggle between charts
        graph_toggle_btns = TailChartToggle(parent=self)

        # Tabs to hold each tail candidate
        self.config_tabs = ConfigTab(parent=self)

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
        self.button_box.accepted.connect(self.close)  # noqa

        vlayout.addWidget(self.button_box)
        self.update_plot()

    def update_plot(self) -> None:

        self.sc.axes.cla()
        tcs = []
        tcds = []

        # fit tail
        for config in self.tail_candidates:

            gb_tail_type = config.gb_tail_type
            tail_params = config.gb_tail_params

            if gb_tail_type.constant_btn.isChecked():

                tail_constant = tail_params.constant_config.sb_tail_constant.spin_box.value()
                decay = tail_params.constant_config.sb_decay.spin_box.value()
                attach = tail_params.constant_config.sb_attach.spin_box.value()
                projection = tail_params.constant_config.sb_projection.spin_box.value()

                tc = cl.TailConstant(
                    tail=tail_constant,
                    decay=decay,
                    attachment_age=attach,
                    projection_period=projection
                ).fit_transform(self.triangle)

            elif gb_tail_type.curve_btn.isChecked():

                curve_config = tail_params.curve_config

                curve = curve_alias[curve_config.curve_type.combo_box.currentText()]
                fit_from = curve_config.fit_from.spin_box.value()
                fit_to = curve_config.fit_to.spin_box.value()
                extrap_periods = curve_config.extrap_periods.spin_box.value()
                errors = fit_errors[curve_config.bg_errors.checkedButton().text()]
                attachment_age = curve_config.attachment_age.spin_box.value()
                projection_period = curve_config.projection.spin_box.value()

                tc = cl.TailCurve(
                    curve=curve,
                    fit_period=(
                        fit_from,
                        fit_to
                    ),
                    extrap_periods=extrap_periods,
                    errors=errors,
                    attachment_age=attachment_age,
                    projection_period=projection_period

                ).fit_transform(self.triangle)

                tcd = cl.TailCurve(
                    curve=curve,
                    fit_period=(
                        fit_from,
                        fit_to
                    ),
                    extrap_periods=extrap_periods,
                    errors=errors,
                    attachment_age=attachment_age,
                    projection_period=projection_period

                ).fit(self.triangle)

                tcds.append(tcd)

            elif gb_tail_type.bondy_btn.isChecked():

                bondy = tail_params.bondy_config
                earliest_age = bondy.earliest_age.spin_box.value()
                attachment_age = bondy.attachment_age.spin_box.value()
                projection_period = bondy.projection.spin_box.value()

                tc = cl.TailBondy(
                    earliest_age=earliest_age,
                    attachment_age=attachment_age,
                    projection_period=projection_period
                ).fit_transform(self.triangle)

            elif gb_tail_type.clark_btn.isChecked():

                clark = tail_params.clark_config

                growth = clark_alias[clark.growth.combo_box.currentText()]
                truncation_age = clark.truncation_age.spin_box.value()
                attachment_age = clark.attachment_age.spin_box.value()
                projection_period = clark.projection.spin_box.value()

                tc = cl.TailClark(
                    growth=growth,
                    truncation_age=truncation_age,
                    attachment_age=attachment_age,
                    projection_period=projection_period
                ).fit_transform(self.triangle)

            else:
                raise Exception("Invalid tail type selected.")

            tcs.append(tc)

        if self.toggled_chart == 'curve_btn':

            x = []
            y = []

            for tc in tcs:
                x.append(list(tc.cdf_.to_frame(origin_as_datetime=True)))
                y.append(tc.cdf_.iloc[:len(x), 0].values.flatten().tolist())

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

            y = []
            width = .4
            for tc in tcs:
                tail = tc.tail_.squeeze()
                y.append(tail)

            for i in range(len(y)):
                x = self.config_tabs.tabText(i)

                self.sc.axes.bar(
                    x=x,
                    width=width,
                    height=y[i]
                )

            self.sc.axes.set_ylabel('Tail Factor')
            self.sc.axes.set_title('Tail Factor Comparison')

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
            model = cl.GridSearch(
                cl.TailCurve(),
                param_grid=param_grid,
                scoring=scoring
            ).fit(tri)

            # Plot results
            pvt = model.results_.pivot( # noqa
                columns='curve',
                index='extrap_periods',
                values='score'
            )

            x = list(pvt.index)
            y1 = pvt['exponential']
            y2 = pvt['inverse_power']

            self.sc.axes.cla()

            self.sc.axes.plot(
                x,
                y1,
                label='Exponential'
            )

            self.sc.axes.plot(
                x,
                y2,
                label='Inverse Power'
            )

            self.sc.axes.set_title(
                'Curve Fit Sensitivity to Extrapolation Period'
            )

            self.sc.axes.set_ylabel('Tail factor')
            self.sc.axes.set_xlabel('Extrapolation Periods')
            self.sc.axes.legend()

            self.sc.draw()

        else:

            for config in self.tail_candidates:
                if not config.gb_tail_type.curve_btn.isChecked():
                    self.sc.axes.cla()
                    return

            y = []

            # base

            tcb = cl.Development().fit_transform(self.triangle)
            obs = (tcb.ldf_ - 1).T.iloc[:, 0]
            obs[obs < 0] = np.nan
            ax = np.log(obs).rename('Selected LDF')
            xb = list(ax.index)

            yb = list(np.log(obs).rename('Selected LDF'))

            self.sc.axes.scatter(xb, yb)

            for tc in tcds:

                y.append(
                    list(pd.Series(
                        np.arange(1, tcb.ldf_.shape[-1] + 1) *
                        tc.slope_.sum().values + # noqa
                        tc.intercept_.sum().values, # noqa
                        index=tcb.ldf_.development,
                        name=f'Ages after 36: {round(tc.tail_.values[0, 0], 3)}') # noqa
                    )
                )

            for i in range(len(y)):

                self.sc.axes.plot(
                    xb,
                    y[i],
                    linestyle='--',
                    label=self.config_tabs.tabText(i)
                )

            self.sc.axes.set_xlabel('Development')
            self.sc.axes.set_title('Fit Period Affect on Tail Estimate')
            self.sc.axes.legend()

            self.sc.axes.xaxis.set_major_locator(plt.MaxNLocator(6))

            self.sc.draw()

    def toggle_chart(self, value) -> None:

        self.toggled_chart = value

        self.update_plot()


class TailChartToggle(QWidget):
    def __init__(
            self,
            parent: TailPane = None
    ):
        """
        Holds button box to toggle diagnostic charts on the TailPane. Intended to be extensible,
        will eventually allow users to add their own buttons via extensions.

        :param parent:
        """
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        curve_btn = self.add_chart_button(
            name='curve_btn',
            tool_tip='Development factor comparison',
            icon='graph-down.svg'
        )

        tail_comps_btn = self.add_chart_button(
            name='tail_comps_btn',
            tool_tip='Tail factor comparison',
            icon='bar-chart-2.svg'
        )

        extrap_btn = self.add_chart_button(
            name='extrap_btn',
            tool_tip='Extrapolation',
            icon='curve-graph.svg'
        )

        reg_btn = self.add_chart_button(
            name='reg_btn',
            tool_tip='Fit period comparison',
            icon='scatter-plot.svg'
        )

        for widget in [
            curve_btn,
            tail_comps_btn,
            extrap_btn,
            reg_btn
        ]:
            self.layout.addWidget(widget)

        self.layout.setContentsMargins(
            0,
            40,
            0,
            0
        )

    def add_chart_button(
            self,
            name: str,
            tool_tip: str,
            icon: str
    ) -> QPushButton:

        btn = QPushButton('')
        btn.setIcon(QIcon(ICONS_PATH + icon))
        btn.setToolTip(tool_tip)
        btn.clicked.connect( # noqa
            partial(self.parent.toggle_chart, name)
        )

        return btn


class MplCanvas(FigureCanvasQTAgg):
    """
    Canvas to plot the diagnostic charts.
    """

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
    """
    A Constant tail factor. Corresponds to TailConstant class in the chainladder package.
    """
    def __init__(
            self,
            parent: TailParamsGroupBox = None
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

        for widget in [
            self.sb_tail_constant,
            self.sb_decay,
            self.sb_attach,
            self.sb_projection
        ]:
            self.layout.addWidget(widget)

        self.sb_tail_constant.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.sb_decay.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.sb_attach.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.sb_projection.spin_box.valueChanged.connect(parent.parent.parent.update_plot)


class CurveConfig(QWidget):
    def __init__(
            self,
            parent: TailParamsGroupBox = None
    ):
        """
        Sets the tail candidate parameters for the Curve method. Corresponds to TailCurve in the chainladder package.
        """
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
            single_step=12,
        )

        self.fit_to = FSpinBox(
            label="To: ",
            value=120,
            single_step=12
        )

        for widget in [
            fit_period_label,
            self.fit_from,
            self.fit_to
        ]:
            fit_period.layout.addWidget(widget)

        self.extrap_periods = FSpinBox(
            label="Extrapolation Periods: ",
            value=100,
            single_step=1
        )

        self.errors = FHContainer()
        errors_label = QLabel("Errors: ")
        self.bg_errors = QButtonGroup()
        errors_ignore = QRadioButton("Ignore")
        errors_raise = QRadioButton("Raise")
        errors_ignore.setChecked(True)
        self.bg_errors.addButton(errors_ignore)
        self.bg_errors.addButton(errors_raise)

        for widget in [
            errors_label,
            errors_ignore,
            errors_raise
        ]:
            self.errors.layout.addWidget(widget)

        self.attachment_age = FSpinBox(
            label='Attachment Age: ',
            value=120,
            single_step=1
        )

        self.projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.curve_type.combo_box.setCurrentText("Exponential")

        for widget in [
            self.curve_type,
            fit_period,
            self.extrap_periods,
            self.errors,
            self.attachment_age,
            self.projection
        ]:
            layout.addWidget(widget)

        self.curve_type.combo_box.currentTextChanged.connect(parent.parent.parent.update_plot)
        self.fit_from.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.fit_to.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.extrap_periods.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.bg_errors.buttonToggled.connect(parent.parent.parent.update_plot)  # noqa
        self.attachment_age.spin_box.valueChanged.connect(parent.parent.parent.update_plot)
        self.projection.spin_box.valueChanged.connect(parent.parent.parent.update_plot)


class ClarkConfig(QWidget):
    def __init__(
            self,
            parent: TailParamsGroupBox = None
    ):
        """
        Sets the tail candidate parameters for the Clark method. Corresponds to TailClark in the chainladder package.
        """
        super().__init__()

        self.parent = parent
        tail_pane = parent.parent.parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.growth = FComboBox(
            label="Growth: "
        )

        self.truncation_age = FSpinBox(
            label="Truncation Age: ",
            value=120,
            single_step=12
        )

        self.attachment_age = FSpinBox(
            label="Attachment Age: ",
            value=120,
            single_step=12
        )

        self.projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.growth.combo_box.addItems([
            'Loglogistic',
            'Weibull'
        ])

        for widget in [
            self.growth,
            self.truncation_age,
            self.attachment_age,
            self.projection
        ]:
            layout.addWidget(widget)

        self.growth.combo_box.currentTextChanged.connect(tail_pane.update_plot)
        self.truncation_age.spin_box.valueChanged.connect(tail_pane.update_plot)
        self.attachment_age.spin_box.valueChanged.connect(tail_pane.update_plot)
        self.projection.spin_box.valueChanged.connect(tail_pane.update_plot)


class BondyConfig(QWidget):
    def __init__(
            self,
            parent: TailParamsGroupBox = None
    ):
        """
        Sets the tail candidate parameters for the Bondy method. Corresponds to TailBondy in the chainladder package.
        """
        super().__init__()

        tail_pane = parent.parent.parent

        self.parent = parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.earliest_age = FSpinBox(
            label="Earliest Age: ",
            value=108,
            single_step=12
        )

        self.attachment_age = FSpinBox(
            label="Attachment Age: ",
            value=120,
            single_step=12
        )

        self.projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        for widget in [
            self.earliest_age,
            self.attachment_age,
            self.projection
        ]:
            layout.addWidget(widget)

        self.earliest_age.spin_box.valueChanged.connect(tail_pane.update_plot)
        self.attachment_age.spin_box.valueChanged.connect(tail_pane.update_plot)
        self.projection.spin_box.valueChanged.connect(tail_pane.update_plot)


class TailConfig(QWidget):
    """
    Area where the user can select the tail candidate's type, along with its associated parameters. The user also
    has the option to mark a particular tail candidate as selected for the reserving model.
    """
    def __init__(
            self,
            parent: TailPane = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Group box to select the tail type
        self.gb_tail_type = TailTypeGroupBox(parent=self)

        # Group box to select the tail parameters
        self.gb_tail_params = TailParamsGroupBox(
            parent=self,
            gb_tail_type=self.gb_tail_type
        )

        # Check box to mark the tail candidate as selected
        self.cb_mark_selected = QCheckBox('Mark as selected')

        for widget in [
            self.gb_tail_type,
            self.gb_tail_params,
            self.cb_mark_selected
        ]:
            self.layout.addWidget(widget)


class TailTypeGroupBox(QGroupBox):
    """
    Group box at the top of the tail pane that allows the user to select
    the candidate tail type (constant, curve, Bondy, Clark).
    """
    def __init__(
            self,
            title: str = "Tail Type",
            parent: TailConfig = None
    ):
        super().__init__(title)

        self.parent = parent

        self.layout = QHBoxLayout()

        # Buttons to select the candidate tail type
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
            self.layout.addWidget(button)

        self.setLayout(self.layout)

        # Default selection is tail constant
        self.constant_btn.setChecked(True)


class TailParamsGroupBox(QGroupBox):
    """
    GroupBox containing a stacked widget. This stacked widget is used to toggle sets of parameters specific
    to the tail type selection from the user.
    """
    def __init__(
            self,
            title: str = "Tail Parameters",
            gb_tail_type: TailTypeGroupBox = None,
            parent: TailConfig = None
    ):
        super().__init__(title)

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Button group from the sibling tail type group box
        self.gb_tail_type = gb_tail_type

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

        self.layout.addWidget(self.params_config)

        # Making a selection from the button group triggers the stack widget to change parameter sets.
        self.gb_tail_type.bg_tail_type.buttonToggled.connect(self.set_config) # noqa

    def set_config(self):

        if self.gb_tail_type.constant_btn.isChecked():
            self.params_config.setCurrentIndex(0)
        elif self.gb_tail_type.curve_btn.isChecked():
            self.params_config.setCurrentIndex(1)
        elif self.gb_tail_type.bondy_btn.isChecked():
            self.params_config.setCurrentIndex(2)
        elif self.gb_tail_type.clark_btn.isChecked():
            self.params_config.setCurrentIndex(3)


class ConfigTab(QTabWidget):
    def __init__(
            self,
            parent: TailPane = None
    ):
        """
        A QTabWidget that holds each tail candidate's configuration parameters
        inside a tab.
        """
        super().__init__()

        self.parent = parent

        # corner widget to hold the two corner buttons
        self.add_remove_btns = AddRemoveButtonWidget(
            p_tool_tip='Add tail candidate',
            m_tool_tip='Remove tail candidate'
        )

        self.setCornerWidget(
            self.add_remove_btns,
            Qt.Corner.TopRightCorner
        )

        self.add_remove_btns.add_tab_btn.pressed.connect(self.add_candidate) # noqa
        self.add_remove_btns.remove_tab_btn.pressed.connect(self.remove_candidate)  # noqa

    def add_candidate(self) -> None:
        """
        Add a tail candidate, hold the info in a new tab.
        """

        new_tab = TailConfig(parent=self.parent)

        # Add tab to parent list keeping track of all the tabs
        self.parent.tail_candidates.append(new_tab)

        # Used to get the default name, just the number of current tabs + 1
        tab_count = self.parent.config_tabs.count()

        self.addTab(
            new_tab,
            'Tail ' + str(self.parent.max_tab_idx + 1)
        )

        self.parent.max_tab_idx += 1

        # Focus on the new tab after it is created.
        self.setCurrentIndex(tab_count)

        # The new tab comes with default info, so we want the plots to incorporate it.
        self.parent.update_plot()

    def remove_candidate(self) -> None:
        """
        Removes tail candidate contained by the actively selected tab.
        """

        # Do nothing if there is only 1 tab.
        if self.count() == 1:
            return

        # Use the index of the currently selected tab to remove the associated candidate.
        idx = self.currentIndex()
        self.parent.tail_candidates.remove(self.currentWidget()) # noqa
        self.removeTab(idx)

        # Remove information from the plots.
        self.parent.update_plot()


# Model/View of the individual LDF/CDFs with the tail in a table
class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()

