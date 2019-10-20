import json
import subprocess
from collections import defaultdict
from itertools import takewhile


def format_jq(input_file, output_file):
    with open(output_file, "w") as f:
        subprocess.run(["jq", "-s", ".", input_file], stdout=f)


def read_json(file):
    with open(file, "r") as f:
        content = json.load(f)

    return content


def write_json(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(content, indent=2, ensure_ascii=False))


def create_graph(courses):
    nodes = dict()
    links = list()

    for course in courses:
        nodes[course["code"]] = {
            "id": course["code"],
            "name": course["name"],
            "description": "",
            "degree": 0,
        }

    for course in courses:
        if course["builds_on"]:
            for req in course["builds_on"]:
                links.append(
                    {"source": course["code"], "target": req, "relationship": ""}
                )
                nodes[req]["degree"] += 1
                nodes[course["code"]]["degree"] += 1

    return {"nodes": list(nodes.values()), "links": links}


def find_course_codes(courses):
    codes = defaultdict(int)

    for course in courses:
        code = "".join(takewhile(str.isalpha, course["code"]))
        codes[code] += 1

    return codes


if __name__ == "__main__":
    format_jq("courses.jl", "courses.json")
    format_jq("faculties.jl", "faculties.json")
    file = read_json("courses.json")
    write_json("graph.json", create_graph(file))
    write_json("codes.json", find_course_codes(file))
