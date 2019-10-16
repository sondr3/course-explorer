import scrapy

from courses.items import CourseItem

URL = "https://www.uib.no"


class CoursesSpider(scrapy.Spider):
    name = "courses"
    start_urls = ["https://www.uib.no/emne/"]

    def parse(self, response):
        content = response.css("div.item-list > ul")[0]
        for course in content.xpath("li/a"):
            yield scrapy.Request(
                f"{URL}{course.attrib['href']}", callback=self.parse_course
            )

    @staticmethod
    def parse_course(response):
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

        for i, title in enumerate(content.xpath("h3/text()").getall()):
            if title.lower() == "Tilrådde forkunnskapar".lower():
                sub_content = content[i]
                course["builds_on"] = sub_content.xpath("p/a/text()").getall()
                break

        if not course["builds_on"]:
            course["builds_on"] = None

        return course
