import cv2
import os
import websockets
import asyncio
import subprocess
from tqdm import tqdm
import numpy as np
import time

def load_templates(template_dir):
    templates = {}
    for filename in os.listdir(template_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            template_path = os.path.join(template_dir, filename)
            template = cv2.imread(template_path, 0)
            templates[os.path.splitext(filename)[0]] = template
    return templates

def template_matching(image_path, template_key, templates, threshold=0.8):
    image = cv2.imread(image_path, 0)
    template = templates[template_key]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    
    locations = np.where(result >= threshold)
    
    if len(locations[0]) > 0:
        top_left = (locations[1][0], locations[0][0])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2
        center = (center_x, center_y)
        
        return top_left, bottom_right, center
    else:
        return None, None, None

async def receive_and_save_image():
    uri = "ws://localhost:8000/stream"
    async with websockets.connect(uri) as websocket:
        data = await websocket.recv()

        with open("./tmp/tmp.jpg", "wb") as image_file:
            image_file.write(data)
            # print("画像を受信し、保存しました。")

def tap_center(center):
    if center is None:
        return -1
    adb_command = f"adb shell input tap {center[0]} {center[1]}"
    subprocess.run(adb_command, shell=True)

def tqdm_sleep(seconds, text):
    for _ in tqdm(range(seconds), desc="{:>15}".format(text)):
        time.sleep(1)

async def main():
    template_dir = r"C:\Prj\KanColleLLM\ClassicalModel\template"
    templates = load_templates(template_dir)
    image_path = "./tmp/tmp.jpg"

    steps = [
        ("supply", 5),
        ("all_supply", 5),
        ("toHome", 5),
        ("home_sortie", 5),
        ("sortie-selection_sortie", 5),
        ("1-1-Kinkai", 5),
        ("battle-stage-ok", 5),
        ("battle-start", 20),
        ("tanju", 30),
        ("next", 3),
        ("next", 3),
        ("next", 3),
        ("next", 3),
        ("back", 10),
        ("next", 10),
        ("withdrawal", 5)
    ]

    for i in tqdm(range(100), desc="{:>15}".format("Loop")):
        for template_key, sleep_time in tqdm(steps, desc="{:>15}".format("Total")):
            await receive_and_save_image()
            top_left, bottom_right, center = template_matching(image_path, template_key, templates)
            tap_center(center)
            tqdm_sleep(sleep_time, template_key)

if __name__ == "__main__":
    asyncio.run(main())