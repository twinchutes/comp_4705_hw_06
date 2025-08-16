from streamlit.testing.v1 import AppTest
import os

def test_load():
    os.chdir("monitoring")
    at = AppTest.from_file("app.py").run(timeout = 10)
    assert not at.exception