"""
@Author: kang.yang
@Date: 2023/8/1 11:53
"""
import kytest
from kytest.android import AdrElem


class DemoPage(kytest.Page):
    """APP首页"""
    adBtn = AdrElem(rid='bottom_btn')
    myTab = AdrElem(text='我的')
    spaceTab = AdrElem(text='科创空间')
    setBtn = AdrElem(rid='me_top_bar_setting_iv')
    title = AdrElem(rid='tv_actionbar_title')
    agreeText = AdrElem(rid='agreement_tv_2')
    moreService = AdrElem(text='更多服务')

