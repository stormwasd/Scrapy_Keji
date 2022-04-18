# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyKejiItem(scrapy.Item):
    # 1.id(url哈希值)
    news_id = scrapy.Field()
    # 2.资讯类别
    category = scrapy.Field()
    # 3.链接地址
    content_url = scrapy.Field()
    # 4.标题
    title = scrapy.Field()
    # 5.发布时间
    issue_time = scrapy.Field()
    # 6.标题图片
    title_image = scrapy.Field()
    # 7.网站名
    information_source = scrapy.Field()
    # 8.来源
    source = scrapy.Field()
    # 9.作者
    author = scrapy.Field()
    # 10.内容
    content = scrapy.Field()
    # 11.文章图片
    images = scrapy.Field()
    # 12.爬取时间
    update_time = scrapy.Field()
    # 13.清洗位   0:未清洗  5:清洗过
    cleaning_status = scrapy.Field()
