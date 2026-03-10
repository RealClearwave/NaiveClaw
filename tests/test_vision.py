import unittest
import sys
import os
import base64

# 将 src 目录加入 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tools.vision import capture_screen_base64

class TestVision(unittest.TestCase):
    def test_capture_screen(self):
        # 测试截屏并返回 Base64 字符串
        try:
            b64_str = capture_screen_base64()
            self.assertIsInstance(b64_str, str, "Should return a base64 encoded string")
            self.assertTrue(len(b64_str) > 100, "Base64 string should be reasonably long")
            
            # 测试是否能正常解码
            decoded = base64.b64decode(b64_str)
            self.assertTrue(len(decoded) > 0, "Decoded bytes should not be empty")
        except Exception as e:
            self.fail(f"Capture screen failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
