from faslr.about import AboutDialog


def test_about(qtbot):
    widget = AboutDialog()
    widget.show()
    qtbot.addWidget(widget)

    assert widget.windowTitle() == "About"
    assert widget.parent is None

    widget.ok()