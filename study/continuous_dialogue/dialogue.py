import openai
from retry_func import retry_with_exponential_backoff


# 创建OpenAI客户端
client = openai.OpenAI(
    api_key="sk-VfrpD4ebvQIdIML3hgX6yk7pWpBc8oABBytMS5ouhn1I3orz",
    base_url="https://api.moonshot.cn/v1", )

# 设置模型
model = "moonshot-v1-8k"


@retry_with_exponential_backoff
def completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)


# 定义一个函数来发送问题并获取答案
def ask_question(model, messages, temperature=0.7):
    try:
        # 发送请求并获取响应
        # response = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
        response = completions_with_backoff(model=model, messages=messages, temperature=temperature)

        # 获取回答
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")


# 开始对话
print("欢迎使用Moonshot AI问答小程序！请问有什么可以帮助您的？")

# 初始化对话上下文
messages = [
    {"role": "system", "content": "欢迎使用Moonshot AI问答小程序！请问有什么可以帮助您的？"},
]

# 持续对话，直到用户选择退出
while True:
    # 获取用户输入
    user_input = input("您: ")

    # 更新对话上下文
    messages.append({"role": "user", "content": user_input})

    # 获取AI的回答
    ai_response = ask_question(model, messages)

    # 打印AI的回答
    print(f"Kimi: {ai_response}")

    # 检查用户是否想要退出对话
    if user_input.lower() in ['exit', 'bye', '再见']:
        print("感谢您的使用，再见！")
        break
