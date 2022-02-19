import scrapy
import json
from ..items import JdItem

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

class PachongSpider(scrapy.Spider):
    name = 'pachong'
    allowed_domains = ['www.jd.com']
    url_head = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100018510746&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    url_middle = '&page='
    url_end = '&pageSize=10&isShadowSku=0&fold=1'

    def start_requests(self):
        #爬取100页评论数据（即1000条）
        for i in range(0,100):
            url = self.url_head +self.url_middle + str(i) + self.url_end
            print("当前页面：", url)
            #url='https://club.jd.com/comment/productPageComments.action?&productId=100008348542&score=3&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1'
            yield scrapy.Request(url=url, callback = self.parse)



    def parse(self, response):
        # 爬取每个手机链接
        # response = requests.get(start_urls, headers=headers)
        json_string = response.text
        data = json.loads(json_string)
        comments = data['comments']
        for i in range(len(comments)):
            item = JdItem()
            #jd_nickname = comments[i]['nickname']
            jd_content = comments[i]['content']
            #jd_score = comments[i]['score']
            #jd_time = comments[i]['creationTime']
            # 变字典
            #item["nickname"] = jd_nickname
            item["content"] = jd_content
            #item["score"] = jd_score
            #item["time"] = jd_time
            yield item

