# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikipediaScaperItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    directors = scrapy.Field()
    box_office = scrapy.Field()
    countries = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
