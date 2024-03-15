"""
@Author: kang.yang
@Date: 2023/11/16 17:36
"""
import kytest
from kytest.ios import IosElem
from kytest.image import ImgElem


class ImagePage(kytest.Page):
    searchBtn = IosElem(text="搜索", className="XCUIElementTypeSearchField")
    searchInput = IosElem(className="XCUIElementTypeSearchField")
    searchResult = IosElem(xpath="//Table/Cell[2]")
    schoolEntry = ImgElem(file="../data/校园场馆.png")
