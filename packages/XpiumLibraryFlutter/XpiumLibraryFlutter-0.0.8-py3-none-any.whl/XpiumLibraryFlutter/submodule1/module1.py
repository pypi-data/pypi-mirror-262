#submodule1/module1.py
# -*- coding: utf-8 -*-
from robot.api.deco import keyword
from .module2 import XDrint
from robot.libraries.BuiltIn import BuiltIn

class XPrint:

    def __init__(self):
        self.ne=XDrint()


    @keyword("XPrint Log")
    def XPrint_log(self):
        print("Hello, world! เทสภาษาไทย111")

    def TestModule2(self):
        dasdsadsa = XDrint()  # สร้างอินสแตนซ์ของคลาส Module2
        dasdsadsa.CDCDCD()    # เรียกใช้เมธอด CDCDCD จากอินสแตนซ์นั้น
        self.ne.CDCDCD()

    def XQuit_App(self):
        """ปิดแอพปัจจุบันและปิดเซสชัน"""
        driver = self._current_application()
        driver.quit()

    def Xwitch_Mode(self,mode):
        """Switch Mode to NATIVE_APP OR FLUTTER.
        """
        driver = self._current_application()

        if mode == 'NATIVE_APP':
            driver.switch_to.context('NATIVE_APP')

        if mode == 'FLUTTER':
            driver.switch_to.context('FLUTTER')


    def _current_application(self):
        """คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน"""
        return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()