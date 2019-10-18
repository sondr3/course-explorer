import json


def read_json():
    with open("courses.json", "r") as f:
        content = json.load(f)

    return content


def create_output(courses):
    nodes = list()
    links = list()

    for course in courses:
        nodes.append({"id": course["code"], "name": course["name"], "description": ""})

        if course["builds_on"]:
            for req in course["builds_on"]:
                links.append(
                    {"source": course["code"], "target": req, "relationship": ""}
                )

    return {"nodes": nodes, "links": links}


if __name__ == "__main__":
    file = read_json()
    output = create_output(file)
    print(json.dumps(output))
