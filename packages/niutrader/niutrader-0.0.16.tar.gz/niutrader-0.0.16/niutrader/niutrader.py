import niutrader
from pywinauto import application


def connect_ths(path=r'C:\同花顺软件\同花顺\xiadan.exe'):
    # 同花顺通用客户端
    user = niutrader.use('universal_client')
    # 有些客户端无法通过 set_edit_text 方法输入内容，可以通过使用 type_keys 方法绕过
    user.enable_type_keys_for_editor()

    try:
        # 连接客户端
        user.connect(path)  # 类似 r'C:\htzqzyb2\xiadan.exe'
    except:
        # 自动启动客户端
        application.Application().start(path, timeout=10)
        # 连接客户端
        user.connect(path)

    return user
