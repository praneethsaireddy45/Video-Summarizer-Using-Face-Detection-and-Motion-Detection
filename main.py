# imports has all the common required imports
from imports import *
from Face_Detect_Func import detectfaces
from Face_Detect_Func_Yunet import yunet_face_detection
from GUI import GUI_data
import cv2
import time

# Switch between Haar and YuNet
USE_YUNET = False  # set True to use YuNet

# Converts seconds to hours/minutes/seconds/milliseconds and returns it
def convert_seconds_to_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    milliseconds = int(milliseconds * 1000)
    return "%d.%d.%d.%d" % (
        int(hours),
        int(minutes),
        int(seconds),
        milliseconds
    )

if __name__ == "__main__":
    # Clear terminal
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print("********************** You Have Accessed The Facial And Motion Scanner and Detector *******************************\n\n")

    # Get file / camera input from GUI
    file_loc, selected_input_type, selected_cam_number = GUI_data()

    # Output folders (relative, GitHub-friendly)
    faces_output_dir = os.path.join("output", "faces_detected")
    motion_output_dir = os.path.join("output", "motion_detected")
    os.makedirs(faces_output_dir, exist_ok=True)
    os.makedirs(motion_output_dir, exist_ok=True)

    frame_count = 0

    # Initialize video capture
    if selected_input_type == "Video" and file_loc and file_loc != "No file selected":
        video_capture = cv2.VideoCapture(file_loc)
    else:
        # Real-time camera
        try:
            cam_idx = int(selected_cam_number) if selected_cam_number.strip() != "" else 0
        except ValueError:
            cam_idx = 0
        video_capture = cv2.VideoCapture(cam_idx)

    if not video_capture.isOpened():
        print("Error: Could not open video source.")
        raise SystemExit(1)

    # Initialize variables
    first_frame = None    # Used for motion detection
    frame_count_act = 0   # Actual frame count
    motion_frame_max = 99 # Save one motion frame every 99 frames
    motion_frame = 1      # Used for motion frame frequency
    t2 = 0
    t_avg = 0
    i = 1

    while True:
        # Capture frame-by-frame
        frame_count_act += 1
        frame_count += 1

        # Read frame
        check, frame = video_capture.read()
        if not check:
            print("The video frame is unreadable or ended.")
            break

        # Convert the frame from BGR to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Save the first frame to detect motion
        if first_frame is None:
            first_frame = gray
            continue

        # Timestamp the frame
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0
        Time = str(convert_seconds_to_time(frame_count_act / fps))

        # Call the detection function
        t1 = time.time()
        if USE_YUNET:
            faces, motion, frame_out = yunet_face_detection(
                frame_count, gray, first_frame, frame.copy()
            )
        else:
            faces, motion, frame_out = detectfaces(
                frame_count, gray, first_frame, frame.copy()
            )
        elapsed = time.time() - t1

        t2 = max(elapsed, t2)
        t_avg += elapsed
        i += 1

        # Save the frame with detected faces
        if faces is True:
            cv2.imwrite(
                os.path.join(faces_output_dir, Time + ".jpg"),
                frame_out
            )
            motion_frame += 1

        # Save 1 frame for every `motion_frame_max` frames of motion
        elif motion == 1:
            if motion_frame % motion_frame_max == 0:
                cv2.imwrite(
                    os.path.join(motion_output_dir, Time + ".jpg"),
                    frame_out
                )
            motion_frame += 1

        # If no motion for a long time, reset first_frame
        else:
            if frame_count > 1000:
                first_frame = gray
                frame_count = 0

        # Show output
        cv2.imshow("Video", frame_out)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("User pressed 'q' – exiting.")
            break

    # Performance stats
    tg = t_avg / max(i, 1)

    print("face detection is over")
    print("\nThe maximum time taken by face_detection function is " + str(t2))
    print("\nThe average time taken by face_detection function is " + str(tg))
    print("\n******************* Program Has Ended ********************")

    video_capture.release()
    cv2.destroyAllWindows()
