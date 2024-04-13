from html import escape


def CodeToHtml(ai_response):
    if "```" in ai_response:
        # 假设代码块以 ``` 开头和结尾，我们将这部分文本视为代码
        code_blocks = ai_response.split("```")[1::2]  # 取出所有偶数索引的字符串，即代码块

        # 对代码块进行HTML实体编码，以避免尖括号被解释为HTML标签
        encoded_code_blocks = [escape(code_block, quote=False) for code_block in code_blocks]

        # 构建格式化后的代码块HTML字符串
        formatted_code_blocks = ["<pre><code>" + code_block + "</code></pre>" for code_block in encoded_code_blocks]

        # 将格式化后的代码块连接起来，并添加到回答中
        ai_response = "".join(formatted_code_blocks)

        return ai_response
