import scrapy
import json
from  ..items import JdItem

import requests
import time
headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

#使用代理
def get_proxy():
    '''
    从代理获取ip封装成proxy字典返回
    '''
    api_url = 'http://http.tiqu.alibabaapi.com/getip?num=10&type=1&pack=87805&port=1&lb=1&pb=4&regions='
    ip = requests.get(api_url).text.strip()

    #如果无法获取ip 抛出一个错误
    if ip =='':
        raise  RuntimeError('无法获取代理ip')
    # 拼装成字典格式
    proxies = {'http': f'http://{ip}'}
    print(proxies)
    return proxies


#url地址
def get_links(num):
    '''

    生成num个url地址返回包含url的列表
    '''
    urls = []
    for i in range(1,num+1):
        urls.append(f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100018510746&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1')
    return urls
#返回抓取的页面
def get_data(url):
    '''
       抓取url上的数据，并打印请求链接和返回的响应码
    '''

    # 注意：必须添加allow_redirects=False，防止requests被重定向，导致打印的响应码不准确
    proxies = get_proxy()
    res = requests.get(url=url, headers=headers,
                       allow_redirects=False, proxies=proxies)
    time.sleep(3)
    print('当前请求的链接：', res.url)
    print('当前返回的响应码：', res.status_code)
    print('================================================')

def run(num):
    '''爬虫主函数，抓取num个详情页'''
    links = get_links(num)
    for l in links:
        get_data(l)
#程序入口
if __name__ == '__main__':
    run(5)

 
class PachongSpider(scrapy.Spider):
    name = 'pachong'
    allowed_domains = ['club.jd.com']
    url_head = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100018510746&score=0&sortType=5'
    url_middle = '&page='
    url_end = '&pageSize=10&isShadowSku=0&fold=1'

    def start_requests(self):
        #爬取100页评论数据（即1000条）
        for i in range(0,100):
            url = self.url_head +self.url_middle + str(i) + self.url_end
            print("当前页面：", url)
            yield scrapy.Request(url=url, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [301,302]
            },callback = self.parse)


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
            print("content")
            #item["score"] = jd_score
            #item["time"] = jd_time
            yield item

