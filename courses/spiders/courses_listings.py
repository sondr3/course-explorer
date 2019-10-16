import scrapy

URL = "https://www.uib.no"


class CoursesSpider(scrapy.Spider):
    name = "courses"
    start_urls = ["https://www.uib.no/emne/"]

    def parse(self, response):
        content = response.css("div.item-list > ul")[0]
        for item in content.xpath("li/a"):
            code, name = item.xpath("text()").get().split("/", maxsplit=1)
            yield {
                "code": code.strip(),
                "name": name.strip(),
                "url": f"{URL}{item.attrib['href']}",
            }
