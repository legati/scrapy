# -*- coding: utf-8 -*-
import scrapy, re, time, html
import scrtools

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader
from ncbi.items import NcbiItem
from urllib import parse



class NcbiSeleniumSpider(scrapy.Spider):
  name = "ncbi_selenium"
  allowed_domains = ["ncbi.nlm.nih.gov"]

  # journalName = "Journal Of Clinical Endocrinology And Metabolism"
  # baseURL ='https://www.ncbi.nlm.nih.gov/pmc/?term=%22J%20Clin%20Endocrinol%20Metab%22%5Bjournal%5D'

  #journalName = "Endocrine Reviews"
  #baseURL ='https://www.ncbi.nlm.nih.gov/pmc/?term=%22Endocr%20Rev%22%5Bjournal%5D'

  journalName = "Journal of Vascular Research"
  baseURL = 'https://www.ncbi.nlm.nih.gov/pmc/?term=Journal+of+Vascular+Research'



  i = 0

  def start_requests(self):
    self.driver = webdriver.Chrome('/home/legati/chromedriver')
    self.driver.get(self.baseURL)


  #start of go to specific page

    # pageNo = 0
    # page_field = self.driver.find_element_by_xpath('//input[@id="pageno"]')
    # page_field.clear()
    # page_field.send_keys(pageNo)
    # page_field.send_keys(u'\ue007') #this is simulation of ENTER key
    # self.i = pageNo

  #end of go to specific page


    sel = Selector (text = self.driver.page_source)
    #print(sel.xpath('//div[@class = "rprt"]/div[@class = "rprtnum"]/span/text()').extract())
    toc_urls = sel.xpath('//a[@class="view" and contains(text(), "rticle")]/@href').extract()
    for url in toc_urls:
      url_full = parse.urljoin("https://www.ncbi.nlm.nih.gov/pmc/", url)
      yield scrapy.Request (url_full, callback=self.parse_site_data)

    while True:
      try:
        time.sleep(1)
        next_page =self.driver.find_element_by_xpath('//a[@class="active page_link next"]')
        next_page.click()

        #self.driver.execute_script("arguments[0].click();", next_page)
        self.logger.info('Sleeping for 2 seconds.')
        time.sleep(5)

        self.i=self.i+1
        #print(sel.xpath('//div[@class = "rprt"]/div[@class = "rprtnum"]/span/text()').extract())
        sel = Selector (text = self.driver.page_source)
        toc_urls = sel.xpath('//a[@class="view" and contains(text(), "rticle")]/@href').extract()
        for url in toc_urls:
          url_full = parse.urljoin("https://www.ncbi.nlm.nih.gov/pmc/", url)
          yield scrapy.Request (url_full, callback=self.parse_site_data)


      except NoSuchElementException:
        self.logger.info('No more pages to load.')
        self.driver.quit()
        break



  def parse_site_data (self, response):

    # div_tags = response.xpath('//div[contains(text(),"orrespond")]')

    # if bool(div_tags) != False: # *Corresponsence to, Corresponding author etc cases

    #   for div_elm in div_tags:
    #     eml = div_elm.xpath('a/@data-email').extract_first()

    #     if eml:
    #       auth = div_elm.xpath('text()').extract_first()
    #       auth = html.unescape(auth)
    #       auth = auth.split(' to')[1]
    #       auth = auth.split(',')[0]
    #       auth = auth.strip(' :')
    #       auth = scrtools.get_clean_author(auth)
    #       eml = eml.replace('mailto:', '')
    #       eml = eml[::-1] #reverses the email string

    #       url = response.url

    #       print ('................................................................................')
    #       print (self.i)
    #       print ('.................................................................................')

    #       l = ItemLoader(item=NcbiItem(), response=response)

    #       l.add_value('url', url)
    #       l.add_value('email', eml)
    #       l.add_value('authors', auth)
    #       l.add_value ('journal', self.journalName)
    #       l.add_value ('date',time.strftime("%d/%m/%Y"))
    #       return l.load_item()

    # else: # DIV cor1

    #   print ('passed!!!..............................')

    #   auth = response.xpath('//div[@id="cor1"]/text()').extract_first()
    #   auth = auth.strip('* :')
    #   auth = scrtools.get_clean_author(auth)

    #   eml = response.xpath('//a[contains(@href, "mailto:")]/@data-email').extract_first()
    #   eml = eml[::-1] #reverses the email string
    authors = response.xpath('//div[@class="half_rhythm"]//div[@class="contrib-group fm-author"]/a')
    affl_list = response.xpath('//div[@class = "fm-affl"]')
    affl_list.append(response.xpath('//div[@id="c1-ijerph-06-02258"]'))
    j = 0
    emls = []
    for author in authors:
      j = j + 1
      refs = author.xpath('./following-sibling::sup[count(preceding-sibling::a) =' + str(j) + ']/text()')
      for ref in refs:
        ref_sup = ref.extract()[0]
        for affl in affl_list:
            affl_sup = affl.xpath('./sup/text()').extract_first()
            if  ref_sup == affl_sup:
                auth = author.xpath('./text()').extract_first()
                emls = emls + affl.xpath('./a[@data-email]/text()').extract()
                if emls:
                    for i in range(0,len(emls)):
                        eml = emls[i]
                        eml = eml[::-1]
                        emls[i] = eml
    #if emls:
                        url = response.url


                        l = ItemLoader(item=NcbiItem(), response=response)

                        l.add_value('url', url)
                        l.add_value('email', emls)
                        l.add_value('authors', auth)
                        l.add_value ('journal', self.journalName)
                        l.add_value ('date',time.strftime("%d/%m/%Y"))
                        return l.load_item()


