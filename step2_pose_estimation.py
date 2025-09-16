import cv2
import mediapipe as mp

# MediaPipeの描画ユーティリティとPoseモデルを初期化
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

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
        
        # 検出された骨格を描画
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('MediaPipe Pose Estimation', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()