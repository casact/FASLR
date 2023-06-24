# import sys
#
# import pytest
#
# from faslr.core import FApplication
#
# from pytestqt.qtbot import QtBot
#
#
# @pytest.fixture(scope="session")
# def f_application():
#
#     app = FApplication(sys.argv)
#
#     return app
#
#
# def test_f_application(
#         qtbot: QtBot,
#         f_application: FApplication
# ) -> None:
#
#     app = f_application
#
