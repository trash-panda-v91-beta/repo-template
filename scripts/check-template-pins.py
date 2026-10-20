#!/usr/bin/env python3
"""Assert every version pin in the template files carries a renovate annotation."""
import json
import pathlib
import re

js = json.load(open("renovate.json"))["customManagers"][0]["matchStrings"][0]
pat = re.compile(js.replace("(?<", "(?P<"))

matched = set()
for f in pathlib.Path("template").rglob("*"):
    if not f.is_file():
        continue
    for m in pat.finditer(f.read_text()):
        d = m.groupdict()
        assert d["datasource"] and d["depName"] and d["packageName"], (f, d)
        matched.add((str(f), d["currentValue"]))

version = re.compile(r'=\s*"(\d+\.\d+\.\d+)"')
pinned = {
    (str(f), v)
    for f in pathlib.Path("template").rglob("*")
    if f.is_file()
    for v in version.findall(f.read_text())
}

missing = pinned - matched
assert not missing, f"pins without renovate annotation: {sorted(missing)}"
print(f"{len(matched)} pins annotated, none missing")
