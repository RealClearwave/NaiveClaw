import unittest
import sys
import os

# 将 src 目录加入 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tools.commander import run_command

class TestCommander(unittest.TestCase):
    def test_run_command_success(self):
        # macOS / Linux / Win 都有 echo
        out = run_command("echo hello")
        self.assertEqual(out, "hello", f"Expected 'hello', got '{out}'")

    def test_run_command_error(self):
        # 运行一个不存在的命令
        out = run_command("some_non_existent_command_12345")
        self.assertTrue("Error:" in out or "Exception:" in out or "not found" in out.lower(), 
                        f"Expected error message, got '{out}'")

if __name__ == '__main__':
    unittest.main()
