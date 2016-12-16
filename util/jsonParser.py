import json

import fileOpener as fo


# def checkKeys(keys, vals, one_json):
#     if len(keys) != len(vals):
#         return False
#     for i in range(0, len(keys)):
#         if one_json[keys[i]] != vals[i]:
#             break

def getServiceInfo(type_service, json_path, type_nameservice=None):
    """Returns service infos as a list.

    :rtype: list"""
    f = fo.openFile(json_path)
    content = f.read()
    # content = content.replace("[", "").replace("]", "")
    js = json.loads(content)
    fo.closeFile(f)
    info_list = []
    for s in js:
        if s[u"type"] == type_service and s[u"activeStatus"] == "ACTIVE":
            info_list.append(dict(s))
        if s[u"type"] == type_nameservice and s[u"activeStatus"] == "ACTIVE":
            info_list.append(dict(s))
    return info_list


def getRoleInfo(service_id, json_path):
    """Returns role infos as a list.

    :rtype: list"""
    f = fo.openFile(json_path)
    js = json.loads(f.read())
    fo.closeFile(f)
    info_list = []
    for s in js:
        if s[u"serviceId"] == int(service_id):
            info_list.append(dict(s))
    return info_list


def getNodeInfo(json_path):
    """Returns node infos as a list.

    :rtype: list"""
    f = fo.openFile(json_path)
    js = json.loads(f.read())
    fo.closeFile(f)
    info_list = []
    for s in js:
        info_list.append(dict(s))
    return info_list
