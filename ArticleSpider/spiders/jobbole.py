# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import AtricleItemLoader,JobboleItem



class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        article_node = response.css('#archive .floated-thumb .post-thumb a')
        for article in article_node:
            img = article.css('img::attr(src)').extract_first('')
            post_url = article.css('::attr(href)').extract_first('')
            if len(post_url)>5:
                yield Request(url=parse.urljoin(response.url, post_url),meta={'img':img},callback=self.parsedetail)
                
        next_url = response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)
                
    
    def parsedetail(self,response):
        itemloader= AtricleItemLoader(item=JobboleItem(),response=response)
        itemloader.add_css('title','div.entry-header h1::text')
        itemloader.add_value('image_url',[response.meta.get('img','')])
        itemloader.add_css('content','div.entry')
        itemloader.add_css('createdate','div.entry-meta p::text')
        itemloader.add_css('praise_num','.vote-post-up h10::text')
        
        article_item = itemloader.load_item()
        yield article_item
