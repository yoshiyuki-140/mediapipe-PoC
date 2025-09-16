import cv2

index = 0
while True:
    # index番目のカメラに接続を試みる
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    
    # 接続できなければループを抜ける
    if not cap.isOpened():
        print(f"インデックス {index} にはカメラが見つかりませんでした。")
        break
    
    # カメラの情報を表示
    print(f"インデックス {index} にカメラを検出しました。")
    
    # リソースを解放
    cap.release()
    
    # 次のインデックスへ
    index += 1