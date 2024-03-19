from .base_provider import BaseProvider
from cnlitellm.models import ResponseModel
from zhipuai import ZhipuAI
import tenacity, logging

class ZhipuAIProvider(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    @tenacity.retry(stop=tenacity.stop_after_attempt(1), reraise=True)
    def completion(self, model: str, messages: list, **kwargs) -> ResponseModel:
        # Check if api_key is set, if not, try to get it from kwargs
        if 'api_key' in kwargs:
            self.api_key = kwargs.get('api_key')
            kwargs.pop('api_key')

        self.client = ZhipuAI(api_key=self.api_key)

        result = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
        # convert result to dict

        print(f"ZhipuAIProvider.completion: result={result}")
        logging.info(f"ZhipuAIProvider.completion: result={result}")

        result = result.dict()
        usage = result['usage']

        response =  ResponseModel(
            prompt_tokens=usage['prompt_tokens'],
            completion_tokens=usage['completion_tokens'],
            total_tokens=usage['total_tokens'],
            total_attempts=1,  # Since retries are handled by tenacity
            raw_response=result,
            usage=usage
        )
        return response.to_dict()
        
    
