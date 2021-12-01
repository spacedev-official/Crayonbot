import json


def loadjson(src):
    with open(src, "r", encoding="utf-8") as f:
        return json.load(f)


def savejson(src, data):
    with open(src, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)