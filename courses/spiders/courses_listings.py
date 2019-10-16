import scrapy

from courses.items import CourseItem

URL = "https://www.uib.no"


class CoursesSpider(scrapy.Spider):
    name = "courses"
    start_urls = ["https://www.uib.no/emne/"]

    def parse(self, response):
        content = response.css("div.item-list > ul")[0]
        for course in content.xpath("li/a"):
            yield scrapy.Request(f"{URL}{course.attrib['href']}", callback=self.parse_course)

    def parse_course(self, response):
        course = CourseItem()
        top = response.css("div.content-top > div.block > div.content > div.item-list > ul > li")
        course["code"]= response.css("h1::text").get().strip()
        course["name"] = top[2].css("span::text")[1].get().strip()
        course["url"] = response.url

        return course

