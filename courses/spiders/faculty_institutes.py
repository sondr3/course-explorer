import scrapy

from courses.items import FacultyItem

URL = "https://www.uib.no/om/73841/fakulteter-og-institutter"


class UiB(scrapy.Spider):
    name = "faculties"
    start_urls = [URL]

    def parse(self, response):
        content = response.css("div.tabs-content")
        faculties = content.xpath("div")

        for fac in faculties:
            faculty = FacultyItem()
            faculty["name"] = fac.xpath("h2/text()").get().strip()
            faculty["institutes"] = fac.xpath("div/ul")[0].xpath("li/a/text()").getall()

            for i, institute in enumerate(faculty["institutes"]):
                if institute == "Institutt for biovitenskap":
                    faculty["institutes"][i] = "Institutt for biovitenskap (BIO)"
                    break

            yield faculty
