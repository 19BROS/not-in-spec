"""Census of a Sphinx XML folder: which nodes, API objects and field shapes the reader meets.

    uv run python core/examples/sphinx/census.py core/examples/sphinx/trio/xml

A dev tool for adding a new library, not part of the reader. Field shapes follow SPEC §6.1:
A = field_body > bullet_list, B = field_body > paragraph, C = field_body > definition_list.
"""

import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

_SHAPES = {"bullet_list": "A", "paragraph": "B", "definition_list": "C"}
_PROSE_CHILDREN = {"paragraph", "bullet_list", "enumerated_list", "note", "warning"}


def main(root: Path) -> None:
    tags: Counter[str] = Counter()
    objtypes: Counter[str] = Counter()
    shapes: Counter[str] = Counter()
    rubrics: Counter[str] = Counter()
    containers: Counter[str] = Counter()
    absolute: Counter[str] = Counter()
    prose_after_desc = 0
    files = sorted(root.rglob("*.xml"))
    for path in files:
        tree = ET.parse(path)
        for el in tree.iter():
            tag = el.tag
            tags[tag] += 1
            if el.get("source", "").startswith("/"):
                absolute[tag] += 1
            if tag == "desc":
                objtypes[f"{el.get('domain')}:{el.get('objtype')}"] += 1
            elif tag == "rubric":
                rubrics["".join(el.itertext()).strip()[:30]] += 1
            elif tag == "container":
                containers[el.get("classes", "")] += 1
            elif tag == "field":
                label = el.find("field_name")
                name = "".join(label.itertext()).split() if label is not None else []
                body = el.find("field_body")
                first = body[0].tag if body is not None and len(body) else "empty"
                shapes[f"{name[0] if name else '?'}:{_SHAPES.get(first, first)}"] += 1
            elif tag == "section":
                kids = [k.tag for k in el]
                if "desc" in kids:
                    last = max(i for i, k in enumerate(kids) if k == "desc")
                    prose_after_desc += any(k in _PROSE_CHILDREN for k in kids[last:])
    addresses = sum(len(re.findall(r"at 0x[0-9a-f]{6,}", p.read_text("utf-8"))) for p in files)
    print(f"documents: {len(files)}")
    print("tags:", ", ".join(f"{t}={n}" for t, n in tags.most_common()))
    print("desc objtypes:", dict(objtypes.most_common()))
    print("field name:shape:", dict(shapes.most_common()))
    print("rubrics:", dict(rubrics.most_common(12)))
    print("containers:", dict(containers.most_common()))
    print("absolute source= paths on:", dict(absolute))
    print("sections with prose after a desc:", prose_after_desc)
    print("'at 0x...' addresses:", addresses)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
