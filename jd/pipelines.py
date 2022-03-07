# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql

def dbHandle():
    conn = pymysql.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "11",
        charset = "utf8",
        use_unicode = False
    )
    return conn

class JdPipeline(object):
    #填入你的地址
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE mysql")
        #插入数据库
        sql = "INSERT INTO jdd(用户名,评论,星级,评论时间) VALUES (%s,%s,%s,%s)"
        try:
            cursor.execute(sql,
                           (item['nickname'], item['content'], item['score'],item['time']))
            cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        return item


