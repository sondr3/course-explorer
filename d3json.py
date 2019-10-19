import json


def read_json():
    with open("courses.json", "r") as f:
        content = json.load(f)

    return content


def create_output(courses):
    nodes = dict()
    links = list()

    for course in courses:
        nodes[course['code']] = {"id": course["code"], "name": course["name"], "description": "", "degree": 0}

    for course in courses:
        if course["builds_on"]:
            for req in course["builds_on"]:
                links.append(
                    {"source": course["code"], "target": req, "relationship": ""}
                )
                nodes[req]['degree'] += 1
                nodes[course['code']]['degree'] += 1

    return {"nodes": list(nodes.values()), "links": links}


if __name__ == "__main__":
    file = read_json()
    output = create_output(file)
    print(json.dumps(output))
