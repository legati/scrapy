# -*- coding: utf-8 -*-
import scrapy, re, time, html
import scrtools

from selenium import webdriver
from scrapy import log
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader
from jvir.items import JvirItem
from urllib import parse

class JvirSeleniumSpider(scrapy.Spider):
    name = "jvir_selenium"
    allowed_domains = ["www.jvir.org"]
    journalName = "Journal of Vascular and Interventional Research"

    def __init__(self):
        self.baseURL = 'http://www.jvir.org/issue/S1051-0443(10)X0014-8' #'http://www.jvir.org/issue/S1051-0443(07)X6058-5'
        self.start_urls = [self.baseURL]


        self.driver = webdriver.Chrome('/home/legati/chromedriver')
        self.driver.wait = WebDriverWait(self.driver, 2)
        self.output = open('jvir.csv', 'at')
        headers = ['url', 'email', 'authors', 'journal', 'date']
        self.output.write(','.join(headers) + '\n')
        self.log('Init finished')


    def parse(self, response):
        self.log('--------------Parse invoked-------------------')
        self.driver.get(response.url)
        issue_page = Selector(text = self.driver.page_source)
        self.parse_issue(issue_page)
        
        while True:
            try:
                time.sleep(1)
                next_page_url = parse.urljoin('http://www.jvir.org', issue_page.xpath('//div[@class="nextIssue"]/a/@href').extract_first())
                self.driver.get(next_page_url)

                self.logger.info('Sleeping for 2 seconds.')
                time.sleep(2)

                issue_page = Selector(text = self.driver.page_source)
                self.parse_issue(issue_page)
            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_issue(self, issue_page):
        time.sleep(1)
        self.log("Parsing the issue")
        article_urls = issue_page.xpath('//div[@class="articleCitation"]//div[@class="article-details"]//a/@href[contains(., "fulltext")]').extract()
        article_urls = set(article_urls)
        for article_url in article_urls:
            full_url = parse.urljoin('http://www.jvir.org', article_url)
            self.driver.get(full_url)
            print(self.driver.current_url)
            article_page = Selector(text = self.driver.page_source)
            self.parse_items(article_page)


    def parse_items(self, article_page):
        self.log('---------Parse_items invoked-----------')
        authors = article_page.xpath('//div[@class = "authorGroup"]/div[@class = "author"]')
        for author in authors:
            eml = author.xpath('.//a[@class = "email"]/@href').extract_first()
            if eml:
                auth = author.xpath('.//a[@class="openAuthorLayer layerTrigger"]/text()').extract_first()

                journal = self.journalName
                date = time.strftime("%d/%m/%Y")
                url = self.driver.current_url
                eml = eml.replace('mailto:', '')

                self.output.write(",".join([url, eml, auth, journal, date]) + '\n')
