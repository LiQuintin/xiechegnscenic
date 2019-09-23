# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from xiechengscenic.items import XiechengscenicItem
import pymysql


class XiechengscenicPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='47.112.212.177',
            port=3306,
            user='rdcBackers',
            passwd='rdc123',
            db='rdc_travel_talking'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        spot_introduction = pymysql.escape_string(item['spot_introduction'])
        insert_sql = "INSERT INTO big_data_scenic(id, preview, title, location, score, spot_introduction, traffic_information) VALUES (" \
                     "'%d', '%s', '%s', '%s', '%f', '%s', '%s')" % (
        item['id'], item['preview'], item['title'], item['location'], item['score'], spot_introduction, item['traffic_information'])
        self.cursor.execute(insert_sql)
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

