import kytest


if __name__ == '__main__':
    # 执行多个用例文件，主程序入口

    # # android
    # kytest.main(
    #     path="tests/test_adr.py",
    #     serial=["UJK0220521066836", "30301cb9"],
    #     package="com.qizhidao.clientapp",
    #     strategy="split_parallel"
    # )

    # # api
    # kytest.main(
    #     path="tests/test_api.py",
    #     project='pc官网',
    #     api_host='https://app-test.qizhidao.com'
    # )

    # # IOS
    # kytest.main(bundle_id="com.qizhidao.company")

    # # image
    # kytest.main(
    #     udid='00008101-000E646A3C29003A',
    #     bundle_id='com.tencent.xin'
    # )

    # # web
    kytest.main(
        project='平台官网',
        path="tests/test_web.py",
        web_host="https://www-test.qizhidao.com/",
    )
