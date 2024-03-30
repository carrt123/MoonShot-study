import datetime

import requests
from openai import OpenAI
from typing import Optional

output_path = "./output"
client = OpenAI(
    api_key="sk-VfrpD4ebvQIdIML3hgX6yk7pWpBc8oABBytMS5ouhn1I3orz",
    base_url="https://api.moonshot.cn/v1",
)
model = "moonshot-v1-8k"


def get_requirement() -> Optional[str]:
    requirement = input("请输入图片需求：\n")
    if not requirement or requirement in ["exit", "quit"]:
        return None

    return requirement


def generate_filename():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S")
    return f"{now_str}.png"


def save_img(img_url: str) -> Optional[str]:
    fullpath = f"{output_path}/{generate_filename()}"
    try:
        print(f"正在保存图片到 {fullpath}")
        img_data = requests.get(img_url).content
        with open(fullpath, "wb") as handler:
            handler.write(img_data)

    except Exception as error:
        print(f"保存文件失败: {error}")
        return None

    print(f"图片已保存到 {fullpath}")
    return fullpath


def generate_img(requirement: str):
    try:
        print("正在生成图片...")
        response = client.images.generate(
            model=model,
            prompt=requirement,
            size="1024x1024",
            response_format="url",
            quality="standard",
        )

        img_url = response.data[0].url
        print("图片生成成功！")
        save_img(img_url)
    except Exception as error:
        print(f"生成图片失败: {error}")
