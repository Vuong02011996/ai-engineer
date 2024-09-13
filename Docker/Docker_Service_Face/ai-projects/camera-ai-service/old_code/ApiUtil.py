#!/usr/bin/env python
# vim: noexpandtab tabstop=4 shiftwidth=4 softtabstop=0

# util for http api

import sys
import json


def kv_to_pyobj(kvstr) -> (int, dict):
    pyobj = {}
    lines = kvstr.splitlines()
    for line in lines:
        sline = line.strip()
        if len(sline) == 0:
            continue
        kv = sline.split("=")
        if len(kv) != 2 or len(kv[0]) == 0:
            return -1, {}

        pobj = pyobj
        key = ""
        arridx = -1
        names = kv[0].split(".")
        for name in names:
            if arridx != -1:
                if len(pobj) < arridx:
                    return -2, {}
                elif len(pobj) == arridx:
                    pobj.append({})
                elif type(pobj[arridx]) is not dict:
                    return -3, {}
                pobj = pobj[arridx]
                arridx = -1
            elif len(key) != 0:
                if key not in pobj:
                    pobj[key] = {}
                elif type(pobj[key]) is not dict:
                    return -4, {}
                pobj = pobj[key]

            if len(name) == 0 or name[0] == "[":
                return -5, {}
            i = name.find("[")
            if i < 0:
                key = name
                arr = ""
            else:
                key = name[:i]
                arr = name[i:]
            while len(arr) > 0:
                if arr[0] != "[":
                    return -11, {}
                i = arr.find("]")
                if i < 2:
                    return -12, {}
                num = arr[1:i]
                arr = arr[i + 1 :]
                if len(num) == 0 or len(num) > 8 or not num.isdigit:
                    return -13, {}
                num = int(num)
                if num < 0:
                    return -14, {}
                if arridx != -1:
                    if len(pobj) < arridx:
                        return -15, {}
                    elif len(pobj) == arridx:
                        pobj.append([])
                    elif type(pobj[arridx]) is not list:
                        return -16, {}
                    pobj = pobj[arridx]
                    arridx = num
                else:
                    if key not in pobj:
                        pobj[key] = []
                    elif type(pobj[key]) is not list:
                        return -17, {}
                    pobj = pobj[key]
                    arridx = num

        if arridx != -1:
            if len(pobj) < arridx:
                return -21, {}
            elif len(pobj) == arridx:
                pobj.append(kv[1])
            else:
                pobj[arridx] = kv[1]
        elif key in pobj and type(pobj[key]) is not str:
            return -22, {}
        else:
            pobj[key] = kv[1]
    return 0, pyobj


def kv_to_jsonstr(kvstr) -> (int, str):
    ret, pyobj = kv_to_pyobj(kvstr)
    if ret < 0:
        return ret, ""
    jsonstr = json.dumps(pyobj, indent=4)
    return 0, jsonstr


if __name__ == "__main__":
    kvstr = """
foo.bar=1
foo.bar2=
foo.arr[0]=20
foo.arr[1]=30
foo.kk[0].vv[0][0]=30
foo.kk[0].vv[0][1]=30
foo.kk[0].vv[1][0]=30
foo.kk[0].vv[1][1]=30
"""
    ret, jsonstr = kv_to_jsonstr(kvstr)
    if ret < 0:
        print("conv failed, ret %d" % ret)
        sys.exit(0)
    print(jsonstr)
