"""
@Author: kang.yang
@Date: 2023/11/16 17:36
"""
import kytest
from kytest.ios import IosElem


class DemoPage(kytest.Page):
    adBtn = IosElem(label='close white big')
    myTab = IosElem(label='我的')
    setBtn = IosElem(label='settings navi')
    about = IosElem(text="关于企知道")
