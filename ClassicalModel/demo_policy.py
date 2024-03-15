import cv2
import os
import websockets
import asyncio
import subprocess

def load_templates(template_dir):
    templates = {}
    for filename in os.listdir(template_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            template_path = os.path.join(template_dir, filename)
            template = cv2.imread(template_path, 0)
            templates[os.path.splitext(filename)[0]] = template
    return templates

def template_matching(image_path, template_key, templates):
    image = cv2.imread(image_path, 0)
    template = templates[template_key]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    
    # 矩形の中心点を計算
    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2
    center = (center_x, center_y)
    
    return top_left, bottom_right, center

async def receive_and_save_image():
    uri = "ws://localhost:8000/stream"  # WebSocket接続のURI
    async with websockets.connect(uri) as websocket:
        # サーバーからのバイナリデータ（JPEG画像）を受信
        data = await websocket.recv()

        # 受信したデータをファイルに保存
        with open("./tmp/tmp.jpg", "wb") as image_file:
            image_file.write(data)
            print("画像を受信し、保存しました。")


def tap_center(center):
    adb_command = f"adb shell input tap {center[0]} {center[1]}"
    subprocess.run(adb_command, shell=True)

# イベントループを実行して、画像受信関数を呼び出す
asyncio.run(receive_and_save_image())

# テンプレートの読み込み
template_dir = r"C:\Prj\KanColleLLM\ClassicalModel\template"
templates = load_templates(template_dir)

# 画像とテンプレートキーの指定
image_path = "./tmp/tmp.jpg"
template_key = "sortie"

# テンプレートマッチングの実行
top_left, bottom_right, center = template_matching(image_path=image_path, template_key="home_sortie", templates=templates)

# 結果の表示
print(f"Matching coordinates: Top-left: {top_left}, Bottom-right: {bottom_right}")
print(f"Center point: {center}")
# 中心座標をタップ
# tap_center(center)

top_left, bottom_right, center = template_matching(image_path=image_path, template_key="sortie-selection_sortie", templates=templates)
# 中心座標をタップ
tap_center(center)