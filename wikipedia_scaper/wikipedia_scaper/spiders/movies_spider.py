import scrapy
import os
import re
import requests

from ..items import WikipediaScaperItem

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class MoviesSpider(scrapy.Spider):
    name = "movies_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_highest-grossing_films#Highest-grossing_films"
    ]

    def parse(self, response):
        movie_rows = response.css('table.wikitable tbody tr')

        for row in movie_rows[1:]:
            movie_link = row.css('td i a::attr(href)').get()
            if movie_link:
                full_url = response.urljoin(movie_link)
                yield scrapy.Request(url=full_url, callback=self.parse_movie)

    def parse_movie(self, response):
        infobox = response.css('table.infobox.vevent')

        title = infobox.css('th.infobox-above::text').get()
        if not title:
            title = infobox.css('th.infobox-above.summary i::text').get()
            print(title)

        directors = self.extract_directors(infobox)
        year = int(infobox.xpath('.//th[div[contains(text(), "Release date")]]/following-sibling::td//li/text()').get().split()[-1])
        box_office = self.extract_numeric_value(infobox.xpath('.//th[contains(text(), "Box office")]/following-sibling::td//text()').get().strip())
        countries = self.extract_countries(infobox)

        image_url = infobox.css('td.infobox-image a img::attr(src)').get()
        if image_url:
            full_image_url = response.urljoin(image_url)

            film_data = {
                'title': title,
                'year': year,
                'directors': directors,
                'box_office': box_office,
                'countries': countries,
                'image_urls': [full_image_url],
            }

            yield WikipediaScaperItem(film_data)

            self.save_image(full_image_url, title)

    def save_image(self, url, filename):
        extension = url.split(".")[-1]
        picture = filename.replace(" ", "_") + "." + extension

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        base_image_dir = os.path.join(project_root, "web", "images")
        final_image_path = os.path.join(base_image_dir, filename.replace(" ", "_"), picture)
        
        current_dir = os.getcwd()
        if os.path.basename(current_dir) == "wikipedia_scaper":
            title = f"images/{filename.replace(' ', '_')}/{picture}"
        else:
            title = f"wikipedia_scaper/images/{filename.replace(' ', '_')}/{picture}"

        os.makedirs(os.path.dirname(title), exist_ok=True)
        os.makedirs(os.path.dirname(final_image_path), exist_ok=True)

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(title, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"saved in {title}")

                with open(final_image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"saved in {final_image_path}")

                return url
            else:
                print(f"error: {response.status_code}")
        except Exception as e:
            print(f"erroe: {e}")

    def extract_directors(self, infobox):
        directors = []

        director_list = infobox.xpath('.//th[contains(text(), "Directed by")]/following-sibling::td//li/a/text()').getall()
        if director_list:
            directors.extend(director_list)
        else:
            director = infobox.xpath('.//th[contains(text(), "Directed by")]/following-sibling::td/a/text()').get()
            if director:
                directors.append(director)

        return directors

    def extract_countries(self, infobox):
        countries = []
        country_list = infobox.xpath('.//th[contains(text(), "Country") or contains(text(), "Countries")]/following-sibling::td//li/text()').getall()
        if country_list:
            countries.extend(country_list)
        else:
            country_text = infobox.xpath('.//th[contains(text(), "Country") or contains(text(), "Countries")]/following-sibling::td/text()').getall()
            if country_text:
                for text in country_text:
                    countries.extend([c.strip() for c in text.split('<br>')])

        return [country.strip() for country in countries]

    def extract_numeric_value(self, raw_value):
        if not raw_value:
            return None

        raw_value = raw_value.replace("$", "").replace(",", "").strip()

        if "million" in raw_value.lower():
            numeric_value = float(re.search(r"[\d.]+", raw_value).group()) * 1_000_000
        elif "billion" in raw_value.lower():
            numeric_value = float(re.search(r"[\d.]+", raw_value).group()) * 1_000_000_000
        else:
            numeric_value = float(re.search(r"[\d.]+", raw_value).group())

        return numeric_value
