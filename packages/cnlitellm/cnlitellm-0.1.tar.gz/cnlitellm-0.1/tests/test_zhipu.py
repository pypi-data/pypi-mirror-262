import sys
import os
import unittest
# 将项目根目录添加到sys.path中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cnlitellm.providers.zhipu import ZhipuAIProvider

class TestZhipuAIProvider(unittest.TestCase):
    def setUp(self):
        # 请将'your_api_key'替换为您的Zhipu AI API密钥
        self.provider = ZhipuAIProvider(api_key='your_api_key')

    def test_completion(self):
        model = 'your_model_name'
        messages = [{'content': '你好，今天天气怎么样？', 'role': 'user'}]
        response = self.provider.completion(model='GLM-4', messages=messages)
        print(response)
        print(response.get_completions())
        # self.assertIsNotNone(response)
        # self.assertIsInstance(response.get_completions(), list)

if __name__ == '__main__':
    unittest.main()
