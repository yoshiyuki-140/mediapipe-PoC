import cv2
import mediapipe as mp

# MediaPipeの描画ユーティリティとPoseモデルを初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

print("ESCキーで終了します。")
# Poseモデルをインスタンス化
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)

        # パフォーマンス向上のため、画像を書き込み不可にしてから処理
        image.flags.writeable = False
        # MediaPipeはRGB画像を期待するため、BGRから変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Poseモデルで画像を処理
        results = pose.process(image)

        # 描画のために画像を書き込み可能に戻し、RGBからBGRに再変換
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
         # ステータス表示用の変数を初期化
        status = "Not Sweeping"

        # 骨格のランドマークが検出されていれば座標を処理
        try:
            landmarks = results.pose_landmarks.landmark
            
            # 1. 関連する関節の座標を取得
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            # 2. 「箒を握っているか」を判定 (両手首のX座標とY座標が近いか)
            is_holding = abs(left_wrist.x - right_wrist.x) < 0.15 and \
                         abs(left_wrist.y - right_wrist.y) < 0.15

            # 3. 「掃く構えをしているか」を判定 (両手首が両肩の平均より下にあるか)
            avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            is_posing = left_wrist.y > avg_shoulder_y and right_wrist.y > avg_shoulder_y

            # 4. 2つの条件が満たされたらステータスを更新
            if is_holding and is_posing:
                status = "Sweeping!"

        except:
            # ランドマークがうまく取れなかった場合などは何もしない
            pass

        # 画面にステータスを表示
        cv2.putText(image, f"STATUS: {status}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 検出された骨格を描画
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('MediaPipe Pose Estimation', image)

        # ESCキーが押されたらループを抜ける
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()