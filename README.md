# Video-Summarizer-Using-Face-Detection-and-Motion-Detection
A Python-based intelligent video summarization system that identifies motion, detects faces, and automatically saves important frames from CCTV or recorded footage. This helps users quickly review long videos by extracting only the meaningful parts.

It uses:

Haar Cascades for fast face detection

YuNet (ONNX) for more accurate face detection (optional)

Frame differencing + thresholds for motion detection

Tkinter GUI to simplify input selection
eatures
Face Detection

Detects multiple faces per frame

Supports:

Haar Cascade frontend

YuNet ONNX model (high accuracy)

 Motion Detection

Uses background subtraction

Extracts frames only when significant movement occurs
