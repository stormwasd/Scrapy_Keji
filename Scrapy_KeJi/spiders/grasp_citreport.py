"""
@Description :
@File        : grasp_citreport
@Project     : Scrapy_KeJi
@Time        : 2022/4/10 23:30
@Author      : LiHouJian
@Software    : PyCharm
@issue       :
@change      :
@reason      :
"""

import scrapy
from scrapy.utils import request
from Scrapy_KeJi.items import ScrapyKejiItem
from Scrapy_KeJi import upload_file
from datetime import datetime


class GraspCitreportSpider(scrapy.Spider):
    name = 'grasp_citreport'
    allowed_domains = ['www.citreport.com']
    start_urls = ['https://www.citreport.com/news/sci/index.php?page=1']
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

    def parse(self, response):
        url_list = response.xpath(
            "//div[@class='article-item']/div[@class='article-info']/a[2]/@href").extract()
        titles = response.xpath(
            "//div[@class='article-item']/div[@class='article-info']/a/h3[@class='multiline-text-overflow']/text()").extract()
        pub_time_list = response.xpath(
            "//div[@class='article-item']/div[@class='article-info']/div[@class='article-time']/text()").extract()
        for i in range(len(url_list)):
            url = url_list[i]
            req = scrapy.Request(
                url, callback=self.parse_detail, dont_filter=True)
            news_id = request.request_fingerprint(req)
            title = titles[i]
            pub_time = pub_time_list[i]
            req.meta.update({"news_id": news_id})
            req.meta.update({"title": title})
            req.meta.update({"pub_time": pub_time.split(' ')[0]})
            yield req
        next_url = response.xpath(
            "//div[@class='pg']/a[@class='nxt']/@href").extract()
        if next_url:
            yield scrapy.Request(url=next_url[-1], callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        news_id = response.meta['news_id']
        title = response.meta['title']
        pub_time = response.meta['pub_time']
        source = response.xpath(
            "//div[@class='cl']/p[@class='authors']/span[2]/text()").extract_first().split(': ')[1]
        content = ''.join(response.xpath(
            "//div[@class='post-content clearfix']|//section[@class='content']|//td[@id='article_content']").extract())
        content_img = response.xpath(
            "//tr/td[@id='article_content']/div[@id='copy_area']/p/img/@src|//td[@id='article_content']/p/img/@src|//section[@class='content']//img/@src").extract()
        if content_img:
            content_img_list = list()
            for index, value in enumerate(content_img):
                img_name = title + str(index)
                res = upload_file.send_file(value, img_name, self.headers)
                if res['msg'] == 'success':
                    content = content.replace(value, res['url'][0])
                    content_img_list.append(res['url'][0])
                else:
                    self.logger.info(f'内容图片 {value} 上传失败，返回数据：{res}')

            imgs = ','.join(content_img_list)
        else:
            imgs = None

        item = ScrapyKejiItem()
        item['news_id'] = news_id
        item['category'] = '科技'
        item['content_url'] = response.url
        item['title'] = title
        item['issue_time'] = pub_time
        item['title_image'] = None
        item['information_source'] = '科技快报网'
        item['content'] = content
        item['source'] = source
        item['author'] = None
        item['images'] = imgs
        item['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['cleaning_status'] = 0
        self.logger.info(item)
        yield item


if __name__ == '__main__':
    import scrapy.cmdline as cmd
    cmd.execute(['scrapy', 'crawl', 'grasp_citreport'])
