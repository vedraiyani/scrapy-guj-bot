# -*- coding: utf-8 -*-
import scrapy
import ast
import json
import math

class ToScrapeMagazineSpider(scrapy.Spider):
    name = "toscrape-magazine"
    
    auther = ''#'jay-vasavada'
    magazine = 'business-plus'#'ravi-purti'
    magazine_url = 'https://www.gujaratsamachar.com/api/magazine/{}?pageIndex='.format(magazine)
    article_url = 'https://www.gujaratsamachar.com/api/article-details/{}/'.format(magazine)

    initial = True


    start_urls = [
        magazine_url+str(1),
    ]

    # def start_requests(self):
    #     urls = [
    #         'https://www.gujaratsamachar.com/api/magazine/shatdal?pageIndex=1'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(type(eval(response.body)))
        # print(type(eval(response.body.decode("utf-8"))))
        # print(type(ast.literal_eval(response.body)))
        # print(type(ast.literal_eval(response.body.decode("utf-8"))))
        # print(type(json.loads(response.body)))
        # print(type(json.loads(response.body.decode("utf-8"))))
        # yield {'body':response.body.decode("utf-8")}
        docs = json.loads(response.body.decode("utf-8"))
        doc_urls = [ToScrapeMagazineSpider.article_url + doc["articleUrl"] for doc in docs["data"]["documents"] if doc["articleUrl"].find(ToScrapeMagazineSpider.auther) != -1]
        if len(doc_urls) != 0:
            yield from response.follow_all(doc_urls, self.parse_article)

        if ToScrapeMagazineSpider.initial == True:
            ToScrapeMagazineSpider.initial == False
            total_urls = math.ceil(docs["data"]["totalCount"]/docs["data"]["magazinePerPage"])
            urls = [ ToScrapeMagazineSpider.magazine_url+str(i) for i in range(2, total_urls+1)]
            yield from response.follow_all(urls, self.parse)

    def parse_article(self, response):
        yield json.loads(response.body)


