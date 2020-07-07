#!/usr/bin/env python

import os
import sys
import json


i = json.loads(sys.argv[1])

safeify = lambda x: x.replace(os.path.sep, "_").replace(
    os.path.pardir, "_" * len(os.path.pardir)
)
incertdir = lambda x: os.path.join(i["options"]["certificates_dir"], x)
inkeydir = lambda x: os.path.join(i["options"]["keys_dir"], x)

o = {}
for k, v in list(i.items()):
    if k == "options":
        continue
    o[k] = {}
    o[k]["key"] = {}
    o[k]["key"]["path"] = inkeydir(safeify(k) + ".key")
    o[k]["key"]["data"] = v["key"]
    o[k]["user_may_read"] = v.get("user_may_read", "")
    o[k]["certificate"] = {}
    o[k]["certificate"]["path"] = incertdir(safeify(k) + ".crt")
    o[k]["certificate"]["data"] = v["certificate"]
    o[k]["assembled_certificate"] = {}
    o[k]["assembled_certificate"]["path"] = incertdir(
        "assembled_" + safeify(k) + ".crt"
    )
    o[k]["intermediate_certificates"] = []
    for n, int in enumerate(v["intermediates"]):
        o[k]["intermediate_certificates"].append({})
        o[k]["intermediate_certificates"][-1]["path"] = incertdir(
            ("intermediate_%s_" % n) + safeify(k) + ".crt"
        )
        o[k]["intermediate_certificates"][-1]["data"] = int

print(json.dumps(o), end=" ")
