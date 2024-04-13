from openai import OpenAI

client = OpenAI(
    api_key="sk-VfrpD4ebvQIdIML3hgX6yk7pWpBc8oABBytMS5ouhn1I3orz",
    base_url="https://api.moonshot.cn/v1",
)

model = "moonshot-v1-8k"
messages = [
    {"role": "user", "content": "请帮我帮如下内容翻译成英文:"},
    {"role": "user", "content": "哪一个球队获得最多世界杯冠军."},
]


response = client.chat.completions.create(
    model=model,
    messages=messages,
)

print(response.choices[0].message.content)