# KanColleLLM


(KanColleLLM) C:\Prj\KanColleLLM>adb devices
List of devices attached
f6a19bcb        device



conda create -n KanColleLLM python=3.11

pip install fastapi uvicorn pillow websockets google-generativeai python-dotenv opencv-python

uvicorn ApollonStreamAPI.api.screencap_server:app --host 0.0.0.0 --port 8000


(KanColleLLM) C:\Prj\KanColleLLM>python ApollonStreamAPI\demo\demo_screencap_client.py
画像を受信し、保存しました。

python ClassicalModel\demo_policy.py