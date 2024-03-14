#XpiumLibraryFlutter/__init__.py
# -*- coding: utf-8 -*-
from robot.api.deco import keyword
from .main import MainClass
from .submodule1 import XPrint
from .submodule1 import XDrint
from .submodule2 import Module21
from .submodule2 import Module22

 
__all__ = [ 'XpiumLibraryFlutter','MainClass', 'XPrint', 'XDrint','Module21', 'Module22']



class XpiumLibraryFlutter(
    MainClass,
    XPrint, 
    XDrint,
    Module21,
    Module22
    ):
    """ XpiumLibraryFlutter เป็นไลบรารีสำหรับทดสอบแอปพลิเคชัน Flutter บนมือถือด้วย Robot Framework
        ไลบรารีนี้ได้รับแรงบันดาลใจมาจาก AppiumFlutterLibrary.

        == Flutter Finder ==

        คำสั่งทั้งหมดที่ต้องการการโต้ตอบกับอิลิเมนต์จะต้องหาอิลิเมนต์นั้นก่อน ในวัตถุประสงค์นี้ เราจึงมีตัวกำหนดตำแหน่ง (locators)
        ที่สื่อสารกับฟังก์ชัน findBy ของ FlutterDriver.

        == Locators ==

        โดยปริยาย เมื่อใส่ตัวกำหนดตำแหน่งโดยไม่ระบุ ไลบรารีจะถือว่าตัวกำหนดตำแหน่งนั้นเป็น key ของ FlutterDriver
        ถ้าคุณต้องการใช้ตัวกำหนดตำแหน่งอื่น คุณจะต้องตั้งค่าตัวระบุนั้นๆ ขึ้นมา

        ตัวอย่าง:

        | Click Element    input-button
        | Click Element    text=Input

        ตัวกำหนดตำแหน่งที่สามารถใช้ได้:

        | *Locator*    | *Description*                      |
        | key          | key ของอิลิเมนต์ FlutterDriver.       |
        | text         | ข้อความของอิลิเมนต์.                   |
        | semantics    | ป้ายกำกับ semantics ของอิลิเมนต์        |
        | tooltip      | ข้อความแจ้งเตือนของอิลิเมนต์             |
        | type         | ประเภทของอิลิเมนต์                    |
    """


    def TTTTTT(self):
        """ พิมพ์ข้อความ 'Hello, world!' ลงในคอนโซล แบบไม่ได้แอดคีย์ """
        print("Hello, world! เทสภาษาไทยfdsafadsfsadfdsafdsa")


    @keyword("Hello world12")
    def Hello12(self):
        """ พิมพ์ข้อความ 'Hello, world!' ลงในคอนโซล แบบแอดคีย์ """
        print("Hello, world! Test keyword='Hello, world!'")
