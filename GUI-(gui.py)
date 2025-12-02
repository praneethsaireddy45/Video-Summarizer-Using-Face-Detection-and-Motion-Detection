import tkinter as tk
from tkinter import filedialog

def GUI_data():
    def start_analysis():
        input_type = input_var.get()
        selected_cam = cam_entry.get()
        selected_video = video_location_label.cget("text")
        # Return in this order: file_loc, input_type, cam_no
        return selected_video, input_type, selected_cam

    # Main window
    root = tk.Tk()
    root.title("Theft Scanner GUI")

    # Input type label
    input_label = tk.Label(root, text="Select Input Type:")
    input_label.pack()

    # Radio buttons
    input_var = tk.StringVar(value="Video")
    real_time_radio = tk.Radiobutton(
        root, text="Real-Time Footage",
        variable=input_var, value="Real-Time Footage"
    )
    video_radio = tk.Radiobutton(
        root, text="Video",
        variable=input_var, value="Video"
    )
    real_time_radio.pack()
    video_radio.pack()

    # Camera number
    cam_label = tk.Label(root, text="Enter Camera Number (for Real-Time):")
    cam_label.pack()
    cam_entry = tk.Entry(root)
    cam_entry.insert(0, "0")  # default
    cam_entry.pack()

    # Video file selection
    video_location_label = tk.Label(root, text="No file selected")
    video_location_label.pack()

    def select_video():
        filename = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[
                ("Video files", "*.mp4;*.avi;*.mov;*.mkv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            video_location_label.config(text=filename)

    video_button = tk.Button(root, text="Select Video File", command=select_video)
    video_button.pack()

    # Start button
    start_button = tk.Button(root, text="Start Analysis", command=root.quit)
    start_button.pack()

    # Run the GUI event loop
    root.mainloop()

    # Get values after window closes
    selected_video_location, selected_input_type, selected_cam_number = start_analysis()
    print("Input type:", selected_input_type)
    print("Video file:", selected_video_location)
    print("Camera #:", selected_cam_number)

    return selected_video_location, selected_input_type, selected_cam_number
