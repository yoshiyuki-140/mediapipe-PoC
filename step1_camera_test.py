import cv2

# Webカメラの指定 (0は通常、内蔵カメラ)
cap = cv2.VideoCapture(1)

while cap.isOpened():
    # カメラから1フレームずつ読み込む
    success, image = cap.read()
    if not success:
        print("カメラフレームの読み込みに失敗しました。")
        continue

    # 映像を左右反転させる (自撮り風にするため)
    image = cv2.flip(image, 1)

    # ウィンドウに映像を表示する
    cv2.imshow('Camera Test', image)

    # ESCキーが押されたらループを抜ける
    if cv2.waitKey(5) & 0xFF == 27:
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()