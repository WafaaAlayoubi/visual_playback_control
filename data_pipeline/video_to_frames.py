import cv2
import os
import argparse

def parse_time(time_str):
    """Parses a 'MM:SS' string into total seconds."""
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        raise ValueError("Time format must be MM:SS")

def extract_frames(video_path, start_time_str, end_time_str, output_folder):
    """
    Extracts one frame per second from a video within a specified time range.

    Args:
        video_path (str): Path to the input video file.
        start_time_str (str): Start time in 'MM:SS' format.
        end_time_str (str): End time in 'MM:SS' format.
        output_folder (str): Folder to save the extracted frames.
    """
    # --- 1. Input Validation and Setup ---
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at '{video_path}'")
        return

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        start_sec = parse_time(start_time_str)
        end_sec = parse_time(end_time_str)
    except ValueError as e:
        print(f"Error: Invalid time format. {e}")
        return

    if start_sec >= end_sec:
        print("Error: Start time must be before end time.")
        return

    # --- 2. Video Processing ---
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: Could not determine video FPS. Assuming 30.")
        fps = 30 # A safe default

    print(f"Video Info: '{video_path}'")
    print(f" - FPS: {fps:.2f}")
    print(f" - Extracting from {start_time_str} ({start_sec}s) to {end_time_str} ({end_sec}s)")
    
    # Set the video to the starting second
    cap.set(cv2.CAP_PROP_POS_MSEC, start_sec * 1000)

    saved_frame_count = 0
    
    # --- 3. Frame Extraction Loop ---
    while cap.isOpened():
        # Get the current position in the video
        current_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
        current_sec = current_msec / 1000.0

        if current_sec > end_sec:
            break

        ret, frame = cap.read()
        if not ret:
            break

        # Construct a unique filename
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_filename = os.path.join(
            output_folder, 
            f"{video_name}_time_{int(current_sec // 60):02d}_{int(current_sec % 60):02d}.jpg"
        )
        
        cv2.imwrite(output_filename, frame)
        print(f"Saved frame: {output_filename}")
        saved_frame_count += 1
        
        # Skip ahead by approximately one second's worth of frames
        # This is more efficient than reading every single frame
        for _ in range(int(fps) - 1):
            cap.read()

    print(f"\nExtraction complete. Total frames saved: {saved_frame_count}")
    cap.release()

if __name__ == "__main__":
    # --- 4. Command-Line Argument Parser ---
    parser = argparse.ArgumentParser(description="Extract 1 frame per second from a video in a given time range.")
    parser.add_argument("video_file", type=str, help="Path to the video file.")
    parser.add_argument("start_time", type=str, help="Start time in MM:SS format (e.g., '00:15').")
    parser.add_argument("end_time", type=str, help="End time in MM:SS format (e.g., '00:25').")
    parser.add_argument("-o", "--output", type=str, default="../dataset/source_images", help="Folder to save the frames (default: 'extracted_frames').")

    args = parser.parse_args()

    extract_frames(args.video_file, args.start_time, args.end_time, args.output)

    # python video_to_frames.py ../dataset/raw_videos/output2.avi 00:00 00:06 