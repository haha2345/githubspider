import scrapy
from collections import defaultdict

class GithubtrendingSpider(scrapy.Spider):
    name = "githubtrending"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/trending"]

    def parse(self, response):
        # print(response.body.decode('utf-8'))
        node_list = response.xpath("//a[@class='Link']")
        for node in node_list:
            url = node.xpath("@href").extract()[0]
            # print(url)
            full_url = response.urljoin(url)
            print(full_url)
            yield scrapy.Request(full_url, callback=self.parse_readme)

    def parse_readme(self, response):
        # 获取仓库名称
        repo_name = response.xpath("//strong[@itemprop='name']/a/text()").get()
        watchers = response.xpath("//a[@class='Link Link--muted']/strong/text()").getall()[1].strip()
        forks = response.xpath("//a[@class='Link Link--muted']/strong/text()").getall()[2].strip()
        stars = response.xpath("//a[@class='Link Link--muted']/strong/text()").getall()[0].strip().replace(",", "")  # 去除千位分隔符
        about_info = response.xpath('//p[@class="f4 my-3"]/text()').get()
        about = about_info.strip() if about_info else ""  # 处理 About 信息可能为空的情况
        # 获取仓库链接
        repo_url = response.url

        # 获取语言信息和占比
        language_elements = response.css("ul.list-style-none li span[itemprop='programmingLanguage']::text").getall()
        total_percent = 100
        languages = []
        language_percentages = defaultdict(float)

        for language_element in language_elements:
            language = language_element.strip()
            languages.append(language)

        percentage_elements = response.css(
            "ul.list-style-none li span.Progress-item:not([is='Progress-item'])::attr(aria-label)"
        ).getall()
        for percentage_element in percentage_elements:
            percentage = float(percentage_element.strip().replace("%", ""))
            language_percentages[languages.pop(0)] = percentage
            total_percent -= percentage

        # 处理剩余语言的占比
        if languages:
            language_percentages[languages.pop(0)] = total_percent
        # 尝试获取 README 文件内容，处理几种常见情况
        readme_content = response.xpath('//article[@class="markdown-body entry-content container-lg"]//text()').getall()
        if not readme_content:
            # 尝试查找其他 README 文件链接
            readme_links = response.xpath('//a[contains(@href, "README") or contains(@href, "readme")]/@href').getall()
            for readme_link in readme_links:
                yield scrapy.Request(response.urljoin(readme_link), callback=self.parse_readme_content, meta={"repo_name": repo_name,
                                                                                                              "watchers": watchers,
                                                                                                              "forks": forks,
                                                                                                              "stars": stars,
                                                                                                              "languages": dict(language_percentages),
                                                                                                              "about_info": about,
                                                                                                              "repo_url": repo_url,},)
        else:
            yield {
                "repo_name": repo_name,
                "watchers": watchers,
                "forks": forks,
                "stars": stars,
                "languages": dict(language_percentages),
                "about_info": about,
                "repo_url": repo_url,
                "readme_content": "".join(readme_content).strip(),
            }

    def parse_readme_content(self, response):
        # 获取 README 内容
        readme_content = response.xpath('//article[@class="markdown-body entry-content container-lg"]//text()').getall()

        yield {
            "repo_name": response.meta["repo_name"],
            "watchers": response.meta["watchers"],
            "forks": response.meta["forks"],
            "stars": response.meta["stars"],
            "languages": response.meta["languages"],
            "about_info": response.meta["about_info"],
            "repo_url": response.meta["repo_url"],
            "readme_content": "".join(readme_content).strip(),
        }