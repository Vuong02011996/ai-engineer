# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#
#
# # https://stackoverflow.com/questions/37317140/cutting-out-a-portion-of-video-python
# start_time = 1
# end_time = 100
# # input_path = "/home/gg-greenlab/Videos/test_safe_region.mp4"
# input_path = "/storages/data/DATA/Clip_data/6203743cc5d991baa520b624_safe_region.mp4"
# ffmpeg_extract_subclip(input_path, start_time, end_time,
#                        targetname="/storages/data/DATA/Clip_data/safe_region_Vuongtest1_6203940630f28ed67bee13d8.mp4")

import numpy as np

arr = np.array([1, 3, 4, 5, 6])
indices = np.array([0, 2, 4])

result = np.delete(arr, indices)
print('result: ', result)
arr = ['a', 'c', 'b', 'c']
sub_indices = [1, 2]

# Chuyển mảng ban đầu và mảng con thành hai tập hợp
arr_set = set(range(len(arr)))
sub_indices_set = set(sub_indices)

# Lấy tập hợp chứa các chỉ số còn lại bằng toán tử set difference
result_set = arr_set - sub_indices_set

# Chuyển kết quả từ tập hợp về mảng
result = list(result_set)