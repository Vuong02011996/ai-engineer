from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import math


class Rate2Angle_Converter:
    """

    """
    def __init__(self):

        # self.pitch_rate_samples = np.array([-0.2, -0.15, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0], dtype=float)
        # self.pitch_angle_samples = np.array([90,   85,    80,  60,  50,  45,  40,  35,  20,  10,  0], dtype=float)
        self.pitch_rate_samples = np.array([-0.2, -0.15, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0], dtype=float)
        self.pitch_angle_samples = np.array([90, 85, 80, 60, 50, 45, 40, 30, 15, 5, 0], dtype=float)
        self.pitch_tck = interpolate.splrep(self.pitch_rate_samples, self.pitch_angle_samples)
        self.pitch_xnew = np.linspace(-0.2, 1.0, num=180, endpoint=True)
        self.pitch_ynew = interpolate.splev(self.pitch_xnew, self.pitch_tck, der=0)

        # self.yaw_rate_samples = np.array([0.0, 0.1, 0.2, 0.28, 0.35, 0.4, 0.5, 0.65, 0.8, 1.0], dtype=float)
        # self.yaw_angle_samples = np.array([40, 37, 35, 30, 25, 20, 15, 10, 5, 0], dtype=float)
        self.yaw_rate_samples = np.array(
            [-1.0, -0.6, -0.35, -0.2, -0.15, -0.05, 0.0, 0.1, 0.2, 0.28, 0.35, 0.4, 0.5, 0.65, 0.8, 1.0], dtype=float)
        self.yaw_angle_samples = np.array([91, 90, 75, 60, 50, 45, 40, 37, 35, 30, 25, 20, 15, 10, 5, 0], dtype=float)
        self.yaw_tck = interpolate.splrep(self.yaw_rate_samples, self.yaw_angle_samples)
        self.yaw_xnew = np.linspace(-1.0, 1.0, num=180, endpoint=True)
        self.yaw_ynew = interpolate.splev(self.yaw_xnew, self.yaw_tck, der=0)

    def convert_pitchrate2angle(self, rate):
        index = np.searchsorted(self.pitch_xnew, rate)
        if (index < len(self.pitch_ynew)):
            angle = int(self.pitch_ynew[index])
        else:
            angle = self.pitch_ynew[-1]

        return angle

    def convert_yawrate2angle(self, rate):
        index = np.searchsorted(self.yaw_xnew, rate)
        if (index < len(self.yaw_ynew)):
            angle = int(self.yaw_ynew[index])
        else:
            angle = self.yaw_ynew[-1]

        return angle

    def show_figure(self, pitch=True):

        if pitch:
            plt.plot(self.pitch_rate_samples, self.pitch_angle_samples, 'o', self.pitch_xnew, self.pitch_ynew)
        else:
            plt.plot(self.yaw_rate_samples, self.yaw_angle_samples, 'o', self.yaw_xnew, self.yaw_ynew)

        plt.legend(['data', 'spline-cubic'], loc='best')
        plt.show()


def area_of_triangle(p1, p2, p3):
    a = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    b = ((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2) ** 0.5
    c = ((p3[0] - p2[0]) ** 2 + (p3[1] - p2[1]) ** 2) ** 0.5

    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5

    if c != 0:
        # duong cao tu P1 point to P2P3 line
        h1 = 2 * area / c
    else:
        h1 = 0

    return area, h1


def get_roll_pit_yaw_angles(face_bbox, landmark5):
    angle_converter = Rate2Angle_Converter()

    l_eye = (landmark5[0][0], landmark5[0][1])
    r_eye = (landmark5[1][0], landmark5[1][1])
    nose = (landmark5[2][0], landmark5[2][1])
    l_mouth = (landmark5[3][0], landmark5[3][1])
    r_mouth = (landmark5[4][0], landmark5[4][1])

    mid_left = ((l_eye[0] + l_mouth[0]) / 2, (l_eye[1] + l_mouth[1]) / 2)
    mid_right = ((r_eye[0] + r_mouth[0]) / 2, (r_eye[1] + r_mouth[1]) / 2)
    mid_top = ((l_eye[0] + r_eye[0]) / 2, (l_eye[1] + r_eye[1]) / 2)
    mid_bottom = ((l_mouth[0] + r_mouth[0]) / 2, (l_mouth[1] + r_mouth[1]) / 2)

    l_vec = (mid_left[0] - nose[0], mid_left[1] - nose[1])  # mid_left_vector
    r_vec = (mid_right[0] - nose[0], mid_right[1] - nose[1])  # mid_right_vector
    t_vec = (mid_top[0] - nose[0], mid_top[1] - nose[1])  # mid_top_vector
    b_vec = (mid_bottom[0] - nose[0], mid_bottom[1] - nose[1])  # mid_bottom_vector

    dot_left_right = l_vec[0] * r_vec[0] + l_vec[1] * r_vec[1]
    dot_top_bottom = t_vec[0] * b_vec[0] + t_vec[1] * b_vec[1]

    # ! Runtime warning
    l_area, l_h = area_of_triangle(nose, l_eye, l_mouth)
    r_area, r_h = area_of_triangle(nose, r_eye, r_mouth)
    t_area, t_h = area_of_triangle(nose, l_eye, r_eye)
    b_area, b_h = area_of_triangle(nose, l_mouth, r_mouth)

    if nose[0] <= (face_bbox[0] + face_bbox[2]) / 2:
        yaw_sign = 1
    else:
        yaw_sign = -1

    if (t_h / 17.0) >= (b_h / 15.0):
        pitch_sign = 1
    else:
        pitch_sign = -1

    # if angle of a and b is <= 90, then nose tip inside polygon of (leye, reye, rmouth, lmouth)
    if dot_left_right <= 0:
        if (l_h == 0) or (r_h == 0):
            yaw = 0
        elif l_h >= r_h:
            yaw = r_h / l_h
        else:
            yaw = l_h / r_h

    else:
        if (l_h == 0) or (r_h == 0):
            yaw = 0
        elif l_h >= r_h:
            yaw = -(r_h / l_h)
        else:
            yaw = -(l_h / r_h)

    # yaw = yaw_sign * yaw
    yaw = yaw_sign * angle_converter.convert_yawrate2angle(yaw)

    if abs(yaw) <= 45:

        t_h /= 17
        b_h /= 15

        if dot_top_bottom <= 0:
            if (t_h == 0) or (b_h == 0):
                pitch = 0
            elif b_h <= t_h:
                pitch = b_h / t_h
            else:
                pitch = t_h / b_h
        else:
            if (t_h == 0) or (b_h == 0):
                pitch = 0
            elif b_h <= t_h:
                pitch = -(b_h / t_h)
            else:
                pitch = -(t_h / b_h)

        pitch = pitch_sign * angle_converter.convert_pitchrate2angle(pitch)
        # pitch = pitch_sign * pitch

    else:
        # Using triangle formula to find angle between r_mouth_2_r_eye vector and Oy,
        # or find angle between l_mouth_2_l_eye vector and Oy
        if yaw > 0:
            p1, p2 = r_eye, r_mouth
        else:
            p1, p2 = l_eye, l_mouth

        base = abs(p1[0] - p2[0])
        hy = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5  # hypotenuse
        if p1[0] > p2[0]:  # face up
            pitch = -math.asin(base / hy) * 180.0 / math.pi
        elif p1[0] < p2[0]:  # face down
            pitch = +math.asin(base / hy) * 180.0 / math.pi
        else:
            pitch = 0

    # for roll, using triangle formula to find angle between l_eye_2_r_eye vector and Ox.
    p1, p2 = l_eye, r_eye
    hy = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5  # hypotenuse

    if hy >= 5:
        base = abs(p1[1] - p2[1])
        if p1[1] < p2[1]:
            roll = +math.asin(base / hy) * 180.0 / math.pi
        elif p1[1] > p2[1]:
            roll = -math.asin(base / hy) * 180.0 / math.pi
        else:
            roll = 0
    else:
        roll = 0

    return np.array([roll, pitch, yaw])


def get_Roll_Pitch_Yaw_new(face_bbox, landmark5, MAX_ROLL, MAX_PITCH, MAX_YAW):
    roll_pitch_yaw = get_roll_pit_yaw_angles(face_bbox, landmark5)

    if (
            (abs(roll_pitch_yaw[0]) <= MAX_ROLL)
            and (abs(roll_pitch_yaw[1]) <= MAX_PITCH)
            and (abs(roll_pitch_yaw[2]) <= MAX_YAW)
    ):
        return roll_pitch_yaw
    else:
        return None


front_face_roll_pitch_yaw = [30, 30, 30]


def is_frontal_face(roll_pitch_yaw):
    """
    roll_pitch_yaw: list, e.g [1, 12, 38]
    """
    roll, pitch, yaw =roll_pitch_yaw
    if (abs(roll) > front_face_roll_pitch_yaw[0]) or (abs(pitch) > front_face_roll_pitch_yaw[1])\
            or (abs(yaw) > front_face_roll_pitch_yaw[2]):
        return False
    return True