import json
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import takewhile
from typing import List, Dict, Union, Set


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


@dataclass
class Course:
    id: str
    name: str
    institute: str
    builds_on: Union[List[str], None]
    description: str = ""
    degree: int = 0


@dataclass
class Institute:
    name: str
    courses: Set[str] = field(default_factory=lambda: set())
    total_courses: int = 0


@dataclass
class University:
    name: str
    total_courses: int = 0
    institutes: Dict[str, Institute] = field(default_factory=lambda: defaultdict(str))
    courses: Dict[str, Course] = field(default_factory=lambda: defaultdict(str))

    def build_university(self, courses):
        for course in courses:
            institute = course["institute"] if course.get("institute") else "None"
            course_id = course["id"]
            name = course["name"]
            builds_on = course["builds_on"]

            if not self.institutes[institute]:
                self.institutes[institute] = Institute(institute)

            self.institutes[institute].total_courses += 1
            self.total_courses += 1
            self.courses[course_id] = Course(course_id, name, institute, builds_on)

        self.calculate_degrees()

    def calculate_degrees(self):
        for course in self.courses.values():
            if course.builds_on:
                for req in course.builds_on:
                    self.courses[course.id].degree += 1
                    self.courses[req].degree += 1

    def courses_at_institutes(self):
        output = defaultdict(dict)
        for course in self.courses.values():
            code = "".join(takewhile(str.isalpha, course.id))
            count = output[course.institute].get(code, 0)
            output[course.institute][code] = count + 1

        return output

    def create_graph(self):
        nodes = dict()
        links = list()

        for course in self.courses.values():
            nodes[course.id] = {
                "id": course.id,
                "name": course.name,
                "description": "",
                "degree": course.degree,
            }

            if course.builds_on:
                for req in course.builds_on:
                    links.append(
                        {"source": course.id, "target": req, "relationship": ""}
                    )

        return {"nodes": list(nodes.values()), "links": links}


if __name__ == "__main__":
    format_jq("courses.jl", "courses.json")
    uib = University("Universitetet i Bergen")
    courses_input = read_json("courses.json")
    uib.build_university(courses_input)
    write_json("graph.json", uib.create_graph())
