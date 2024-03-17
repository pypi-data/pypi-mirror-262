# -*- coding: utf-8 -*-
import abc
import io
import tempfile
import time
from io import StringIO
from typing import TYPE_CHECKING, Dict, List, Optional

import pandas as pd
import pywinauto.keyboard
import pywinauto
import pywinauto.clipboard

from niutrader.log import logger
from niutrader.utils.captcha import captcha_recognize
from niutrader.utils.win_gui import SetForegroundWindow, ShowWindow, win32defines
from niutrader.utils.perf import perf_clock

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from niutrader import clienttrader


class IGridStrategy(abc.ABC):
    @abc.abstractmethod
    def get(self, control_id: int) -> List[Dict]:
        """
        获取 gird 数据并格式化返回

        :param control_id: grid 的 control id
        :return: grid 数据
        """
        pass

    @abc.abstractmethod
    def set_trader(self, trader: "clienttrader.IClientTrader"):
        pass


class BaseStrategy(IGridStrategy):
    def __init__(self):
        self._trader = None

    def set_trader(self, trader: "clienttrader.IClientTrader"):
        self._trader = trader

    @abc.abstractmethod
    def get(self, control_id: int) -> List[Dict]:
        """
        :param control_id: grid 的 control id
        :return: grid 数据
        """
        pass

    def _get_grid(self, control_id: int):
        grid = self._trader.main.child_window(
            control_id=control_id, class_name="CVirtualGridCtrl"  # 这里control_id = 1047,就是大片数据的地方
        )
        return grid

    def _set_foreground(self, grid=None):
        try:
            if grid is None:
                grid = self._trader.main
            if grid.has_style(win32defines.WS_MINIMIZE):  # if minimized
                ShowWindow(grid.wrapper_object(), 9)  # restore window state
            else:
                SetForegroundWindow(grid.wrapper_object())  # bring to front
        except:
            pass


class Copy(BaseStrategy):
    """
    通过复制 grid 内容到剪切板再读取来获取 grid 内容
    """
    _need_captcha_reg = True

    def get(self, control_id: int) -> List[Dict]:
        grid = self._get_grid(control_id)  # 返回一个grid对象，main.child_window
        self._set_foreground(grid)  # 放到最前面
        grid.type_keys("^A^C", set_foreground=False)  # 复制粘贴数据
        content = self._get_clipboard_data()  # 这里获取数据，占用时间很长，为什么呢？  # content是str
        return self._format_grid_data(content)

    def _format_grid_data(self, data: str) -> List[Dict]:  # 将str转化成dict，感觉直接输出dataframe比较好呢
        try:
            df = pd.read_csv(
                io.StringIO(data),
                delimiter="\t",
                dtype=self._trader.config.GRID_DTYPE,
                na_filter=False,
                # index_col=[12],
            )
            df = df.loc[:, ~df.columns.str.match('Unnamed')]  # 添加的，删除unamed一列
            return df.to_dict("records")
        except:
            Copy._need_captcha_reg = True

    @perf_clock   # 这里花费了6秒，为什么？
    def _get_clipboard_data(self) -> str:
        # 如果出现验证码，先过验证码
        if Copy._need_captcha_reg:
            if self._trader.app.top_window().window(class_name="Static", title_re="验证码").exists(timeout=1.0):
                file_path = "tmp.png"

                count = 10  # 重试次数
                while count > 0:

                    self._trader.app.top_window().window(control_id=0x965, class_name="Static").capture_as_image().save(file_path)  # 保存验证码，id是2405
                    captcha_num = captcha_recognize(file_path).strip()  # 识别验证码，花费0.3s
                    captcha_num = "".join(captcha_num.split())
                    logger.info("captcha result-->" + captcha_num)

                    if len(captcha_num) == 4:
                        self._trader.app.top_window().window(control_id=0x964, class_name="Edit").type_keys(captcha_num)  # 模拟输入验证码 #id是2404 # 这里原来用的是set_text，改为type_keys，可用正常运行，原来是无法输入内容
                        self._trader.app.top_window().set_focus()
                        pywinauto.keyboard.send_keys("{ENTER}")  # 模拟发送enter，点击确定

                        # try:
                        # 就是这里费时间的，找不到这个控件，多费了很多时间
                        #     logger.info(self._trader.app.top_window().window(control_id=0x966, class_name="Static").window_text())  # 这里control_id是16进制，就是输入框的地方，如果过了验证码，这里就么有了,2406是个啥 ，没找到 呢
                        # except Exception as ex:  # 窗体消失
                        #     # logger.exception(ex)  # 取消后不报错
                        #     break

                    if not self._trader.app.top_window().window(class_name="Static", title_re="验证码").exists(timeout=1.0):
                        break
                    else:
                        count -= 1
                        self._trader.wait(0.1)
                        self._trader.app.top_window().window(control_id=0x965, class_name="Static").click()  # 点击验证码，继续进行下一次验证码识别
                        self._trader.app.top_window().window(control_id=0x964, class_name="Edit").type_keys('')  # 这里还是不能删除，验证码错了他不会自动删除的

            # else:
            #     Copy._need_captcha_reg = False  # 如果没有验证码窗口，设置False，然后取获取粘贴板数据

        # 没有验证码，直接获取数据，如果有验证码，先过验证码，然后获取数据
        # return pywinauto.clipboard.GetData()
        count = 5
        while count > 0:
            try:
                return pywinauto.clipboard.GetData()  #
            # pylint: disable=broad-except
            except Exception as e:
                count -= 1
                logger.exception("%s, retry ......", e)


# class WMCopy(Copy):
#     """
#     通过复制 grid 内容到剪切板再读取来获取 grid 内容
#     """
#
#     def get(self, control_id: int) -> List[Dict]:
#         grid = self._get_grid(control_id)
#         grid.post_message(win32defines.WM_COMMAND, 0xE122, 0)
#         self._trader.wait(0.1)
#         content = self._get_clipboard_data()
#         return self._format_grid_data(content)
#
#
# class Xls(BaseStrategy):
#     """
#     通过将 Grid 另存为 xls 文件再读取的方式获取 grid 内容
#     """
#
#     def __init__(self, tmp_folder: Optional[str] = None):
#         """
#         :param tmp_folder: 用于保持临时文件的文件夹
#         """
#         super().__init__()
#         self.tmp_folder = tmp_folder
#
#     def get(self, control_id: int) -> List[Dict]:
#         grid = self._get_grid(control_id)
#
#         # ctrl+s 保存 grid 内容为 xls 文件
#         self._set_foreground(grid)  # setFocus buggy, instead of SetForegroundWindow
#         grid.type_keys("^s", set_foreground=False)
#         count = 10
#         while count > 0:
#             if self._trader.is_exist_pop_dialog():
#                 break
#             self._trader.wait(0.2)
#             count -= 1
#
#         temp_path = tempfile.mktemp(suffix=".xls", dir=self.tmp_folder)
#         self._set_foreground(self._trader.app.top_window())
#
#         # alt+s保存，alt+y替换已存在的文件
#         self._trader.app.top_window().Edit1.set_edit_text(temp_path)
#         self._trader.wait(0.1)
#         self._trader.app.top_window().type_keys("%{s}%{y}", set_foreground=False)
#         # Wait until file save complete otherwise pandas can not find file
#         self._trader.wait(0.2)
#         if self._trader.is_exist_pop_dialog():
#             self._trader.app.top_window().Button2.click()
#             self._trader.wait(0.2)
#
#         return self._format_grid_data(temp_path)
#
#     def _format_grid_data(self, data: str) -> List[Dict]:
#         with open(data, encoding="gbk", errors="replace") as f:
#             content = f.read()
#
#         df = pd.read_csv(
#             StringIO(content),
#             delimiter="\t",
#             dtype=self._trader.config.GRID_DTYPE,
#             na_filter=False,
#         )
#         return df.to_dict("records")
