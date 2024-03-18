"""
@Author: kang.yang
@Date: 2023/11/16 17:49
"""
import kytest
from kytest.web import WebElem


class IndexPage(kytest.Page):
    """首页"""
    url = "https://www-test.qizhidao.com/"
    loginBtn = WebElem(xpath='(//div[text()="登录/注册"])[1]')
    patentText = WebElem(xpath='//*[text()="查专利"]')


class LoginPage(kytest.Page):
    """登录页"""
    pwdTab = WebElem(xpath='//*[text()="帐号密码登录"]')
    userInput = WebElem(xpath='//input[@placeholder="请输入手机号码"]')
    pwdInput = WebElem(xpath='//input[@placeholder="请输入密码"]')
    accept = WebElem(css=".agreeCheckbox .el-checkbox__inner")
    loginBtn = WebElem(xpath='//*[text()="立即登录"]')
    firstItem = WebElem(xpath="(//img[@class='right-icon'])[1]")
