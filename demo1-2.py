import os
from zhipuai import  ZhipuAI
from openai import OpenAI
api_key = os.getenv('GLM_API_KEY')

#set up model with GLM method
#client = ZhipuAI(api_key= api_key)

#set up model with oepnai method
client = OpenAI(api_key= api_key,
                base_url='https://open.bigmodel.cn/api/paas/v4/',
                )

response = client.chat.completions.create(
    model = 'glm-4-plus',
    messages = [
        {'role': 'user',
         'content':'Can you introduce GLM LLM?'},
    ],
    stream = True
)
#print(response.choices[0].message.content)
for s in response:
    print(s.choices[0].delta.content)

