# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
    
    
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
class MysqlTwistedPipline(object):
    
    def __init__(self,dbpool):
        self.dbpool = dbpool
        
    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,
            
            )
        dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        
        return cls(dbpool)
        
    def process_item(self,item,spider):
        qury = self.dbpool.runInteraction(self.do_insert,item)
        qury.addErrback(self.handererr,item,spider)
        return item


    def do_insert(self,cursor,item):
        insert_sql,params = item.get_insert_sql()
        print('insert_sql:',insert_sql)
        print('params:',params)
        cursor.execute(insert_sql,params)
        
    def handererr(self,failure,item,spider):
        print(failure)