# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class GithubspiderPipeline:

    # def __init__(self):
        # self.file = open('githubspider.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        item_dict = dict(item)
        # 将数据保存为 JSON 文件，文件名可以自定义
        with open("github_trending.json", "a", encoding="utf-8") as f:
            json.dump(item_dict, f, ensure_ascii=False, indent=4)
            f.write("\n")  # 每条数据单独一行
        return item
