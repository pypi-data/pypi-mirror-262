# -*- coding: utf-8 -*-
#XpiumLibraryFlutter.py

from robot.api.deco import keyword
from .main import MainClass
from .submodule1 import XPrint
from .submodule1 import XDrint
from .submodule2 import Module21
from .submodule2 import Module22
# from robot.libraries.BuiltIn import BuiltIn


class XpiumLibraryFlutter(
    MainClass,
    XPrint, 
    XDrint,
    Module21,
    Module22
    ):

    # def __init__(self):
        # self._bi = BuiltIn()

    # def t_quit_app(self):
    #     """ปิดแอพปัจจุบันและปิดเซสชัน"""
    #     driver = self._current_application()
    #     driver.quit()

    # def _current_application(self):
    #     """คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน"""
    #     return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()

    
    def TTTTTT(self):
        """ พิมพ์ข้อความ 'Hello, world!' ลงในคอนโซล แบบไม่ได้แอดคีย์ """
        print("Hello, world! เทสภาษาไทยfdsafadsfsadfdsafdsa")


    @keyword("Hello world12")
    def Hello12(self):
        """ พิมพ์ข้อความ 'Hello, world!' ลงในคอนโซล แบบแอดคีย์ """
        print("Hello, world! Test keyword='Hello, world!'")
