
import scrapy
import json
import requests
from  ..items import JdItem



 
class PachongSpider(scrapy.Spider):
    name = 'pachong'
    allowed_domains = ['club.jd.com']
    def start_requests(self):
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100018510746&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        yield scrapy.Request(url=url, meta={'proxy':'221.10.104.106:4378'})
        
    
    def parse(self, response):
        # 爬取每个手机链接
        # response = requests.get(start_urls, headers=headers)
        json_string = response.text
        print('ok')
        #data = json.loads(json_string)
        jd = json.loads(json_string.lstrip('fetchJSON_comment98vv12345(').rstrip(');')) 
        comments = jd['comments']
        for i in range(len(comments)):
            item = JdItem()
            jd_nickname = comments[i]['nickname']
            jd_content = comments[i]['content']
            jd_score = comments[i]['score']
            jd_time = comments[i]['creationTime']
            # 变字典
            item["nickname"] = jd_nickname
            item["content"] = jd_content
            item["score"] = jd_score
            item["time"] = jd_time
            yield item
