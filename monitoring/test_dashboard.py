from streamlit.testing.v1 import AppTest
import os

def test_load():
    at = AppTest.from_file("app.py").run(timeout = 10)
    assert not at.exception