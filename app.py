from flask import Flask, render_template, request, jsonify
import openai
from retry_func import retry_with_exponential_backoff
from returnCode_func import CodeToHtml
import markdown

app = Flask(__name__)

# 设置OpenAI API密钥
OPENAI_API_KEY = "sk-VfrpD4ebvQIdIML3hgX6yk7pWpBc8oABBytMS5ouhn1I3orz"

# 设置OpenAI客户端
client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)

# 设置模型
model = "moonshot-v1-8k"


@retry_with_exponential_backoff
def completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)


# 定义一个函数来发送问题并获取答案
def ask_question(messages, temperature=0.7):
    try:
        # 发送请求并获取响应
        response = completions_with_backoff(model=model, messages=messages, temperature=temperature)
        # 获取回答
        ai_response = CodeToHtml(response.choices[0].message.content)

        # 返回AI的回答
        return ai_response

    except Exception as e:
        return f"Error: {e}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.form['user_input']
        # 初始化对话上下文
        messages = [
            {"role": "system", "content": "欢迎使用Moonshot AI问答小程序！请问有什么可以帮助您的？"},
            {"role": "user", "content": "在接下来的对话中,请使用Markdown格式输出，但是回答中不需要携带Markdown字样。"},
            {"role": "user", "content": user_input}
        ]

        # 获取AI的回答
        ai_response = markdown.markdown(ask_question(messages))

        # 返回AI的回答
        return jsonify({'ai_response': ai_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
