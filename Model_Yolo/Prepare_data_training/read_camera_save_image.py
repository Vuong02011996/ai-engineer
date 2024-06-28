import cv2
import os


# Function to save video frames as images
def save_frames_from_video(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If the frame was not retrieved, end of the video has been reached
        if not ret:
            break

        # Create a filename for each frame
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")

        # Save the frame as a JPG image
        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()

    print(f"Saved {frame_count} frames to {output_folder}")


if __name__ == '__main__':
    # Path to the video file
    video_path = 'path/to/your/video.mp4'

    # Output folder to save frames
    output_folder = 'path/to/save/frames'

    # Call the function to save frames from the video
    save_frames_from_video(video_path, output_folder)