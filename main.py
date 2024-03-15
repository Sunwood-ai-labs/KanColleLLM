import pathlib
import textwrap
import os
import google.generativeai as genai
from PIL import Image

from dotenv import load_dotenv

load_dotenv(verbose=True)
load_dotenv()


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 画像を開く
img = Image.open(r'demo/received_image.jpg')

# 元のサイズを取得
original_width, original_height = img.size

# サイズを半分にする
new_width = original_width // 2
new_height = original_height // 2

# リサイズ（アスペクト比を維持）
img_resized = img.resize((new_width, new_height))

model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
prompt = """
艦これです
出撃したいです．

座標を下記のフォーマットでください
単位はピクセルです．
---
(X, Y)
"""

prompt = """
艦これです
出撃したいです．

どこをタッチすればいい？
"""

response = model.generate_content([prompt, img])
print(response.text)

# adb shell input touchscreen tap 104 134
# adb shell input tap 468 636