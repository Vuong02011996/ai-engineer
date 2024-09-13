from datetime import datetime


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


def to_epoch(timestamp: str):
    return str(int(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timestamp()))

