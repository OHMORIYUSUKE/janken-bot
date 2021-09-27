import random
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/v1/", methods=['GET'])
def index():
    # 画像のオーバーレイ
    def overlayImage(src, overlay, location):
        overlay_height, overlay_width = overlay.shape[:2]

        # 背景をPIL形式に変換
        src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        pil_src = Image.fromarray(src)
        pil_src = pil_src.convert('RGBA')

        # オーバーレイをPIL形式に変換
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
        pil_overlay = Image.fromarray(overlay)
        pil_overlay = pil_overlay.convert('RGBA')

        # 画像を合成
        pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
        pil_tmp.paste(pil_overlay, location, pil_overlay)
        result_image = Image.alpha_composite(pil_src, pil_tmp)

        # OpenCV形式に変換
        return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)

    #path_janken = "C:/Users/81908/Documents/kadaiJava/se21-bot-OHMORIYUSUKE/softeng_python_api-main/python_api/lec06/chatBot/janken/"
    path_janken = ""

    user_hand = request.args.get('hand', '')
    cpu_hund_number = random.randint(0, 2)
    user_hund_number = int(user_hand)

    result_number = (user_hund_number - cpu_hund_number + 3) % 3
    print(user_hund_number)
    print(cpu_hund_number)

    if result_number == 0:
        img_result = cv2.imread(path_janken + "result_images/draw.png", cv2.IMREAD_UNCHANGED)
    elif result_number == 1:
        img_result = cv2.imread(path_janken + "result_images/lose.png", cv2.IMREAD_UNCHANGED)
    elif result_number == 2:
        img_result = cv2.imread(path_janken + "result_images/win.png", cv2.IMREAD_UNCHANGED)

    # 重ねる画像
    if user_hund_number == 0:
        img_user = cv2.imread(path_janken+"hands_images/gu.png", cv2.IMREAD_UNCHANGED)
    elif user_hund_number == 1:
        img_user = cv2.imread(path_janken + "hands_images/choki.png", cv2.IMREAD_UNCHANGED)
    elif user_hund_number == 2:
        img_user = cv2.imread(path_janken + "hands_images/pa.png", cv2.IMREAD_UNCHANGED)
    print(cpu_hund_number)
    if cpu_hund_number == 0:
        img_cpu = cv2.imread(path_janken+"hands_images/gu.png", cv2.IMREAD_UNCHANGED)
    elif cpu_hund_number == 1:
        img_cpu = cv2.imread(path_janken + "hands_images/choki.png", cv2.IMREAD_UNCHANGED)
    elif cpu_hund_number == 2:
        img_cpu = cv2.imread(path_janken + "hands_images/pa.png", cv2.IMREAD_UNCHANGED)
    # ベース画像
    image = cv2.imread(path_janken+"base.png", cv2.IMREAD_COLOR)
    try:
        image = overlayImage(image, img_cpu, (600,10))
        image = overlayImage(image, img_user, (100, 10))
        image = overlayImage(image, img_result, (250, 320))
    except Exception as e:
        print(e)
    # 結果を出力
    cv2.imwrite(path_janken+"result.jpg", image)

    return redirect('https://github.com/OHMORIYUSUKE')
if __name__ == "__main__":
    app.run()