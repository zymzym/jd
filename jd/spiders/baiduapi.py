import scrapy

class callspider(scrapy.Spider):
    name = 'call'
    def start_requests(self):
        url = ['https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?&access_token=24.71ee39ed701f98f57fa451b719e11778.2592000.1650005908.282335-25486945&charset=UTF-8']
        headers={'Content-Type': 'application/json'}
        body = '{"text":"苹果是一家伟大的公司"}'.encode(encoding='UTF-8',errors='strict')
        print (body)
        yield scrapy.Request(url=url, callback='parse_item',method='POST',headers=headers,body=body)
    def parse_item(self,response):
        json_string = response.text
        print (json_string)