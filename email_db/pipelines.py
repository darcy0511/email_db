# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import traceback

class EmailDbPipeline(object):
    
    #def __init__(self):
    #    pass

    def open_spider(self, spider):
        #print spider.name
        #print spider.custom_settings
        db_name = spider.custom_settings["sqlite3_db"]
        #print "---------start-------"
        
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
 
        fields = " text, ".join(spider.custom_settings['fields_list']) + " text"
        sql = 'create table {table_name} ({fields});'.format(table_name=spider.name,fields=fields)
        try:
            self.cur.execute(sql)
            self.cur.commit()
        except Exception, e:
            traceback.print_exc()

        fields = ",".join(spider.custom_settings['fields_list'])
        values = ",".join(['?']*len(spider.custom_settings['fields_list']))
        self.insert_sql = "insert into {table_name} ({fields}) values ({values})".format(table_name=spider.name,fields=fields,values=values)
        
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):

        self.cur.execute(self.insert_sql,tuple(item.values()))
        return item
