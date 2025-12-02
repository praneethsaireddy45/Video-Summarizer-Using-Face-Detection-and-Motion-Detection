from imports import *
import cv2
import os

def yunet_face_detection(frame_count, gray, first_frame, image):
    # YuNet ONNX model (put the file in models/)
    onnx_path = os.path.join("models", "face_detection_yunet.onnx")

    # Threshold for motion area
    threshold_area = 2000

    # Motion detection (background subtraction)
    delta_frame = cv2.absdiff(first_frame, gray)
    # cv2.imshow('delta_frame', delta_frame)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('thresh', thresh_frame)

    # Clean the frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contours
    cnts, _ = cv2.findContours(
        thresh_frame.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    motion = 0

    for contours in cnts:
        if cv2.contourArea(contours) < threshold_area:
            continue

        motion = 1

        # If ONNX not found, just return motion
        if not os.path.exists(onnx_path):
            return False, motion, image

        # FaceDetectorYN expects size (width, height)
        h, w = image.shape[:2]

        # Make sure image is BGR
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 1:
            image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif channels == 4:
            image_bgr = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        else:
            image_bgr = image

        # Create YuNet detector
        face_detector = cv2.FaceDetectorYN_create(onnx_path, "", (w, h))
        face_detector.setInputSize((w, h))

        # Detect faces
        _, faces = face_detector.detect(image_bgr)
        faces = faces if faces is not None else []

        if faces != []:
            for face in faces:
                x, y, width, height = list(map(int, face[:4]))
                box = (x, y, width, height)
                color = (0, 0, 255)
                thickness = 2
                cv2.rectangle(
                    image_bgr,
                    (box[0], box[1]),
                    (box[0] + box[2], box[1] + box[3]),
                    color,
                    thickness,
                    cv2.LINE_AA
                )
            return True, motion, image_bgr

    return False, motion, image
