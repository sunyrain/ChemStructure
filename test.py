import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from swift.llm import (
    get_model_tokenizer, get_template, inference, ModelType,
    get_default_template_type, inference_stream
)
from swift.utils import seed_everything
import torch

model_type = ModelType.glm4v_9b_chat
template_type = get_default_template_type(model_type)
print(f'template_type: {template_type}')

model, tokenizer = get_model_tokenizer(model_type, torch.float16,
                                       model_kwargs={'device_map': 'auto'})
model.generation_config.max_new_tokens = 256
template = get_template(template_type, tokenizer)
seed_everything(42)

images = ['http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/road.png']
query = 'How far is it from each city?'
response, _ = inference(model, template, query, images=images)
print(f'query: {query}')
print(f'response: {response}')

# Streaming
query = 'Which city is the farthest?'
images = images
gen = inference_stream(model, template, query, images=images)
print_idx = 0
print(f'query: {query}\nresponse: ', end='')
for response, _ in gen:
    delta = response[print_idx:]
    print(delta, end='', flush=True)
    print_idx = len(response)
print()
"""
query: How far is it from each city?
response: The distance from each city to the next one is as follows:

1. From Mata to Yangjiang: 62 kilometers
2. From Yangjiang to Guangzhou: 293 kilometers

So, the total distance from Mata to Guangzhou is 62 kilometers (to Yangjiang) plus 293 kilometers (from Yangjiang to Guangzhou), which equals 355 kilometers.
query: Which city is the farthest?
response: The city that is the farthest away from the current location, as indicated on the road sign, is Guangzhou. It is 293 kilometers away.
"""