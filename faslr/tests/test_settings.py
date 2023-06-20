from faslr.settings import (
    SettingsDialog,
    SettingsListModel
)

def test_settings_list_model(qtbot) -> None:

    settings_list_model = SettingsListModel()

    assert settings_list_model.rowCount() == 0

