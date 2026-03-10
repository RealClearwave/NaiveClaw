import unittest
import sys
import os
import pyautogui

# 将 src 目录加入 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tools.controller import click, type_text, scroll

# 限制 pyautogui 的执行速度，防止测试干扰你的电脑
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

class TestController(unittest.TestCase):
    def test_click_and_move(self):
        # 记录当前位置
        original_x, original_y = pyautogui.position()
        
        # 移动并点击屏幕左上角一段距离 (相对安全的位置)
        # 注意：这里为了不误点危险区域，我们可以不用执行真实的物理点击，但在测试中可以轻微移动验证函数跑通
        try:
            res = click(original_x + 5, original_y + 5)
            self.assertTrue("Clicked at" in res)
        finally:
            # 移回原位
            pyautogui.moveTo(original_x, original_y)

    def test_type_text(self):
        # 我们这里不验证真实的打字效果（因为这会在聚焦窗口打字），只验证函数可以调用且返回结果正确
        res = type_text("test")
        self.assertEqual(res, "Typed: 'test'")

if __name__ == '__main__':
    unittest.main()
