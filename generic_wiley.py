# -*- coding: utf-8 -*-
import scrapy, re, time, html

from scrtools import *

from scrapy.loader import ItemLoader
from wiley.items import WileyItem
from urllib import parse

class GenericWileySpider(scrapy.Spider):
  name = "generic_wiley"
  allowed_domains = ["onlinelibrary.wiley.com"]
  
  #IMMUNOLOGY

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/imr.2003.191.issue-1/issuetoc'] 
  # journalName = 'Immunological Reviews' #DONE

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1002/art.v48:1/issuetoc'] 
  # journalName = 'Arthritis & Rheumatology' #Done

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/all.2003.58.issue-1/issuetoc'] 
  # journalName = 'Allergy' # SOMETHING WRONG - FIND OUR and RE-SCRAP

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/cmi.2003.5.issue-1/issuetoc'] 
  # journalName = 'Cellular Microbiology' #DONE

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1002/immu.v33:1/issuetoc'] 
  # journalName = 'European Journal of Immunology' # DONE

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/cea.2003.33.issue-1/issuetoc'] 
  # journalName = 'Clinical & Experimental Allergy' #DONE

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/imm.2003.108.issue-1/issuetoc'] 
  # journalName = 'Immunology' #DONE

  start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/cdr.2000.18.issue-1/issuetoc'] 
  journalName = 'Cardiovascular Therapeutics'


  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = ''

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = ''

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = ''

  def parse(self,response):
    toc_urls = response.xpath('//a[contains(@href, "abstract")]/@href').extract()
    for url in toc_urls:
      yield scrapy.Request (response.urljoin(url), callback=self.parse_site_data)
      

    next_page = response.xpath('//a[@class="next" and @id="nextLink"]/@href').extract_first()
    
    if next_page is not None:
      next_page = response.urljoin(next_page)
      yield scrapy.Request(response.urljoin(next_page), callback=self.parse)



  def parse_site_data (self, response,):

    auth_repl = ('Dr ', 'Professor', 'Associate', 'Prof. Dr. med.')

    #case we do not have envelop icon next to the author name
    if response.xpath('//h3[@class="article-header__authors-name"]/span[@class="icon icon__article-header icon__email"]').extract():

      #case email address is linked to the author name
      if response.xpath('//div[@class="article-header__correspondence-to"]').extract() is None:

        

        li_tags = response.xpath('//li[@class="article-header__authors-item"]')

        for li_elm in li_tags:
          eml = li_elm.xpath('//a[contains(@href,"mailto:")]/@href').extract_first()

          if eml:
            eml = eml.replace('mailto:', '')
            eml = parse.unquote(eml)

            auth = li_elm.xpath('@data-author-name').extract_first()
            
            for au_rpl_item in auth_repl:
              auth = auth.replace(au_rpl_item, '')
            
            auth = auth.strip(', ')
            auth = get_clean_author (auth)

        url = response.url

        l = ItemLoader(item=WileyItem(), response=response)
        l.add_value('url', url)
        l.add_value('email', eml)
        l.add_value('authors', auth)
        l.add_value ('journal', GenericWileySpider.journalName)
        l.add_value ('date',time.strftime("%d/%m/%Y"))


        return l.load_item()

      else: #case email is not linked to author name

        auth_col = response.xpath('//span[@class="icon icon__article-header icon__email"]/parent::h3/parent::li/@data-author-name').extract()
        eml_col = response.xpath('//a[@title="Link to email address" and contains(@href, "mailto:")]/@href').extract()

        if eml_col:
          if auth_col:
            for i in range(len(eml_col)):

              eml = eml_col[i]
              eml = eml.replace('mailto:', '')
              eml = parse.unquote(eml)

              if (len(auth_col)-1) >= i:
                auth = auth_col[i]
              else:
                auth = "????"

              for au_rpl_item in auth_repl:
                auth = auth.replace(au_rpl_item, '')
                auth = auth.strip(', ')    
                auth = get_clean_author(auth)


              
              url = response.url

              l = ItemLoader(item=WileyItem(), response=response)
              l.add_value('url', url)
              l.add_value('email', eml)
              l.add_value('authors', auth)
              l.add_value ('journal', GenericWileySpider.journalName)
              l.add_value ('date',time.strftime("%d/%m/%Y"))

              return l.load_item()


    else: #case we have author name in string with email

      auth = response.xpath('//div[@class="article-header__correspondence-to"]/p/text()').extract_first()
      eml = response.xpath('//a[@title="Link to email address" and contains(@href, "mailto:")]/@href').extract_first()

      if eml:
        if auth:

          eml = eml.replace('mailto:', '')
          eml = parse.unquote(eml)

          for au_rpl_item in auth_repl:
            auth = auth.split(',')[0]
            auth = auth.replace(au_rpl_item, '')
            auth = auth.strip(', ')    
            auth = get_clean_author(auth)

          if bool(auth.strip('\t\r\n ')) == False: # case we have <br> after Correpondece word
            auth = response.xpath('//div[@class="article-header__correspondence-to"]/p').extract_first()
            auth = auth.split("<br>")[1]
            auth = auth.split(",")[0]
            auth = get_clean_author(auth)



          url = response.url

          l = ItemLoader(item=WileyItem(), response=response)
          l.add_value('url', url)
          l.add_value('email', eml)
          l.add_value('authors', auth)
          l.add_value ('journal', GenericWileySpider.journalName)
          l.add_value ('date',time.strftime("%d/%m/%Y"))

          return l.load_item()





  #ENDOCRINOLOGY

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1002/dmrr.v19:1/issuetoc'] 
  # journalName = 'Diabetes/Metabolism Research and Reviews' 

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/jne.2003.15.issue-1/issuetoc'] 
  # journalName = 'Journal of Neuroendocrinology' 

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/pdi.2003.4.issue-1/issuetoc'] 
  # journalName = 'Pediatric Diabetes' 

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/cen.2003.58.issue-1/issuetoc'] 
  # journalName = 'Clinical Endocrinology' 

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/ija.2003.26.issue-1/issuetoc'] 
  # journalName = 'International Journal of Andrology' 

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/andr.2012.1.issue-1/issuetoc'] 
  # journalName = 'Andrology' # Done

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/jdi.2010.1.issue-1-2/issuetoc'] 
  # journalName = 'Journal of Diabetes Investigation' # Done

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/jch.2003.5.issue-1/issuetoc'] 
  # journalName = 'The Journal of Clinical Hypertension' # Done

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1002/jand.2003.24.issue-1/issuetoc'] 
  # journalName = 'Journal of Andrology' # Done


  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/jdb.2009.1.issue-1/issuetoc'] 
  # journalName = 'Journal of Diabetes' # Done

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 




  #AGING

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/ace.2002.1.issue-1/issuetoc'] 
  # journalName = 'Aging Cell' 

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/ics.2003.25.issue-1-2/issuetoc'] 
  # journalName = 'International Journal of Cosmetic Science' 

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 

  
  #PHARMACOLOGY

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1002/med.v23:1/issuetoc']
  # journalName = 'Medicinal Research Reviews'

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/bph.2003.138.issue-1/issuetoc']
  # journalName = 'British Journal of Pharmacology'

  # start_urls = ['http://onlinelibrary.wiley.com/doi/10.1111/adb.2003.8.issue-1/issuetoc']
  # journalName = 'Addiction Biology'