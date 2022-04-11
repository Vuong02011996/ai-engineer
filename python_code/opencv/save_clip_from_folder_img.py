import cv2
import time
from glob import glob
from vidgear.gears import WriteGear
from moviepy.editor import *


def list_images_to_video_write_gear(video_name, list_image):
    output_params = {"-vcodec": "libx264", "-crf": 0, "-preset": "fast"}
    # Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
    writer = WriteGear(output_filename=video_name, logging=True, **output_params)
    for image in list_image:
        img = cv2.imread(image)
        # write gray frame to writer
        writer.write(img)
    writer.close()


def images_to_clip_moviepy(list_image, video_name):
    start_time = time.time()
    clip = ImageSequenceClip(list_image, fps=25)
    clip.write_videofile(video_name)
    print("cost: ", time.time() - start_time)


def list_images_to_video_cv2(video_name, list_image):
    frame = cv2.imread(list_image[0])
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name,
                            cv2.VideoWriter_fourcc(*'vp80'),  # X264, MJPG, MPEG, 'vp80', MP4V
                            25, (width, height))
    for image in list_image:
        img = cv2.imread(image)
        video.write(img)
    video.release()


def check_save_video():
    folder_frame = "/media/vuong/AI1/Data_clover/Image/test_video/Sleepless_Region_0"
    video_name = folder_frame + '/video_cv2.webm'
    list_image = glob(folder_frame + "/*.png")
    list_image.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    start_time = time.time()
    list_images_to_video_cv2(video_name, list_image)
    print("image to video cost : ", time.time() - start_time)


if __name__ == '__main__':
    check_save_video()