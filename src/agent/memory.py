import json
import os

class Memory:
    def __init__(self, memory_file="naiveclaw_memory.json"):
        """
        初始化记忆存储。默认保存在当前目录的 naiveclaw_memory.json 中。
        """
        self.memory_file = memory_file
        self.data = self._load()

    def _load(self):
        """从本地文件加载记忆。"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save(self):
        """将当前记忆写入本地文件持久化。"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def save_memory(self, key: str, value: str):
        """
        保存特定的键值对记忆。
        例如可以保存特定软件的坐标，或执行某项任务的经验。
        """
        self.data[key] = value
        self._save()
        return f"Memory saved: [{key}] -> [{value}]"

    def get_memory(self, key: str):
        """获取特定属性的记忆。"""
        return self.data.get(key)
        
    def get_all(self):
        """返回所有记忆内的数据字典。"""
        return self.data
