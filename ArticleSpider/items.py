# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose
import datetime

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def returnvalue(value):
    return value

def getdate(value):
    value = value.replace('.','').strip()
    try:
        timestr = datetime.datetime.strftime(value,'%Y%m%d')
    except:
        timestr = datetime.datetime.now()
    return str(timestr)

class AtricleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
class JobboleItem(scrapy.Item):
    title = scrapy.Field()
    image_url=scrapy.Field(
        output_processor=MapCompose(returnvalue),
        )
    praise_num=scrapy.Field()
    createdate = scrapy.Field(
        input_processor=MapCompose(getdate),
        )
    content = scrapy.Field()
    
    def get_insert_sql(self):
        insert_sql = '''
            insert into jobbole_article(title,createdate,image_url,praise_num,content) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(praise_num)
        '''
        image_url = ''
        if self['image_url']:
            image_url = self['image_url'][0]
        params = (
            self['title'],self['createdate'],image_url,self['praise_num'],self['content'],
            )
        
        return insert_sql,params

