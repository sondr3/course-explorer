import scrapy

from courses.items import CourseItem

URL = "https://www.uib.no"


def find_dependent_courses(content):
    result = []
    for i, title in enumerate(content.xpath("h3/text()").getall()):
        if title.strip().lower() == "Tilrådde forkunnskapar".lower():
            sub_content = content[i].xpath("p/a")
            for dep_course in sub_content:
                if dep_course.attrib["href"].startswith("/nb/emne"):
                    result.append(dep_course.xpath("text()").get().strip())

            return result

    return None


class CoursesSpider(scrapy.Spider):
    name = "courses"
    start_urls = ["https://www.uib.no/emne/"]

    def parse(self, response):
        content = response.css("div.item-list > ul")[0]
        for course in content.xpath("li/a"):
            yield scrapy.Request(
                f"{URL}{course.attrib['href']}", callback=self.parse_course
            )

    def parse_course(self, response):
        course = CourseItem()
        top = response.css(
            "div.content-top > div.block > div.content > div.item-list > ul > li"
        )
        course["name"] = response.css("h1::text").get().strip()
        course["code"] = top[2].css("span::text")[1].get().strip()
        course["url"] = response.url
        course["builds_on"] = None

        if response.css("div.fs-error"):
            return course

        content = response.css("div#uib-tabs-emnebeskrivelse > div")
        course["builds_on"] = find_dependent_courses(content)
        institute = response.css("div.uib-study-belongs-to").xpath("a")
        course["institute"] = (
            institute.xpath("text()").get().strip() if institute else None
        )

        return course
