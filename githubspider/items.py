# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    repo_name = scrapy.Field()
    watchers = scrapy.Field()
    forks = scrapy.Field()
    stars = scrapy.Field()
    languages = scrapy.Field()  # 存储语言及占比的字典
    readme_content = scrapy.Field()
    about_info = scrapy.Field()
    repo_url = scrapy.Field()
    pass
