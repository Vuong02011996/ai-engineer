#!/usr/bin/env python
# vim: noexpandtab tabstop=4 shiftwidth=4 softtabstop=0

# HTTP API : subscribe snap ( event with picture )

import sys
import datetime
import traceback
import requests


def read_one_part(raw, boundary) -> tuple[int, list, str]:
    # <1> read part header
    data = b""
    idx = 0
    while True:
        data += raw.read(8)
        idx = data.find(b"\r\n\r\n")
        if idx == 0:
            data = data[4:]
            continue
        if idx > 0:
            break

    # <2> parse part header, get Content-Length
    cntlen = -1
    headers = data[: idx + 4].decode().split("\r\n")
    for hd in headers:
        if hd[:14].lower() == "content-length":
            cntlen = int(hd[15:])
    if cntlen < 0:
        return -1, [], "content len %d too small" % cntlen

    # <3> read body
    data = data[idx + 4 :]
    needlen = cntlen - len(data)
    if needlen > 0:
        data += raw.read(needlen)
    try:
        resultData = data.decode()
    except UnicodeDecodeError:
        resultData = data

    return 0, headers, resultData


def subscribe_snap(devip, user, password, event_codes) -> tuple[int, str]:
    url = (
        "http://%s/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[%s]&heartbeat=5"
        % (devip, event_codes)
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    print(url)
    try:
        response = requests.get(
            url,
            auth=requests.auth.HTTPDigestAuth(user, password),
            stream=True,
            headers=headers,
        )
        if response.status_code != 200:
            return response.status_code, response.text
        print(
            "status code %d, Content-Type : [%s]"
            % (response.status_code, response.headers["Content-Type"])
        )

        # read boundary
        contenttype = response.headers["Content-Type"]
        idx = contenttype.find("boundary=")
        if idx < 0:
            return -1, "not multipart"
        boundary = contenttype[idx + 9 :]

        # read and deal with received data
        while True:
            ret, hds, kvstr = read_one_part(response.raw, boundary)
            if ret < 0:
                return -1, "read one part failed, " + kvstr
            if kvstr[:9].lower() == "heartbeat":
                print(
                    "[%s] recv Heartbeat"
                    % datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                )
                continue
            print(
                "[%s] recv event, len %d"
                % (datetime.datetime.now().strftime("%m-%d %H:%M:%S"), len(kvstr))
            )

            # save json-event and picture in current directory
            # saving a json file and a picture is overwritten
            if isinstance(kvstr, str):
                with open("json-event.txt", "w+") as f:
                    f.write(kvstr)
            elif isinstance(kvstr, bytes):
                with open("picture.jpg", "wb+") as f:
                    f.write(kvstr)
    except Exception:
        traceback.print_exc()
        return -1, "exception"
    return ret.status_code, ret.text


if __name__ == "__main__":
    # device info
    devip = "14.241.88.21"
    user = "kbvision"
    password = "123abc456"
    # event
    event_codes = "All"
    if len(sys.argv) >= 2:
        devip = sys.argv[1]
    if len(sys.argv) >= 3:
        user = sys.argv[2]
    if len(sys.argv) >= 4:
        password = sys.argv[3]
    if len(sys.argv) >= 5:
        event_codes = sys.argv[4]

    # snapshot
    status, kvstr = subscribe_snap(devip, user, password, event_codes)
    if status != 200:
        print("subscribe snap failed, status %d, kvstr %s" % (status, kvstr))
        sys.exit(0)
    print("info [%s]" % kvstr)
