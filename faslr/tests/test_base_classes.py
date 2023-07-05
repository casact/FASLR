from faslr.base_classes import (
    FDoubleSpinBox,
    FSpinBox,
    FComboBox,
    FHContainer
)

from pytestqt.qtbot import QtBot


def test_f_double_spin_box(qtbot:QtBot) -> None:

    f_double_spin_box = FDoubleSpinBox(
        label="My Spin Box",
        value=.01,
        single_step=.01
    )

    qtbot.addWidget(f_double_spin_box)

    assert f_double_spin_box.label.text() == "My Spin Box"

    assert f_double_spin_box.spin_box.value() == .01

    # Simulate click up
    f_double_spin_box.spin_box.stepUp()

    assert f_double_spin_box.spin_box.value() == .02

    # Simulate click down

    f_double_spin_box.spin_box.stepDown()

    assert f_double_spin_box.spin_box.value() == .01


def test_f_spin_box(qtbot: QtBot) -> None:

    f_spin_box = FSpinBox(
        label="My Spin Box",
        value=1,
        single_step=1
    )

    qtbot.addWidget(f_spin_box)

    assert f_spin_box.label.text() == "My Spin Box"

    assert f_spin_box.spin_box.value() == 1

    # Simulate click up

    f_spin_box.spin_box.stepUp()

    assert f_spin_box.spin_box.value() == 2

    # Simulate click down

    f_spin_box.spin_box.stepDown()

    assert f_spin_box.spin_box.value() == 1


def test_f_combo_box(qtbot: QtBot) -> None:

    f_combo_box = FComboBox(
        label="My Combo Box"
    )

    qtbot.addWidget(f_combo_box)

    assert f_combo_box.label.text() == "My Combo Box"


def test_fh_container(qtbot: QtBot) -> None:

    fh_container = FHContainer()

    qtbot.addWidget(fh_container)
