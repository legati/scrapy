# -*- coding: utf-8 -*-
import scrapy, re, time

import scrtools
from scrapy.loader import ItemLoader
from ncbi.items import NcbiItem

class GenNcbiSpider(scrapy.Spider):
  name = "gen_ncbi"
  allowed_domains = ["ncbi.nlm.nih.gov"]

  #GET TOC
  #[response.urljoin(i) for i in response.xpath('//a[@class="arc-issue"]/@href').extract()]

  
  # journalName = "Frontiers in Immunology"
  # start_urls = [

  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/248098/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/263639/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/284458/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/209608/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/209606/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/209609/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/218553/',
  #              'https://www.ncbi.nlm.nih.gov/pmc/issues/232451/']

  journalName = "CPT: Pharmacometrics and Systems Pharmacology"
  start_urls = [
               'https://www.ncbi.nlm.nih.gov/pmc/issues/220931/'
               ]

 

  

  def parse(self,response):
    toc_urls = response.xpath('//a[@class="view" and contains(text(), "rticle")]/@href').extract()

    for url in toc_urls:
      yield scrapy.Request (response.urljoin(url), callback=self.parse_site_data)
      

    # next_page =  response.xpath('//a[@class="navlink" and contains(text(), "ext")]/@href').extract_first()
    # if next_page is not None:
    #   yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

  def parse_site_data (self, response):

    div_tags = response.xpath('//div[contains(text(),"orrespond")]')

    if bool(div_tags) != False: # *Corresponsence to, Corresponding author etc cases

      for div_elm in div_tags:
        eml = div_elm.xpath('a/@data-email').extract_first()

        if eml:
          auth = div_elm.xpath('text()').extract_first()
          auth = html.unescape(auth)
          if " to" in auth:
            auth = auth.split(' to')[1]
          elif "author:" in auth:
            auth = auth.split('author: ')[1]
          else:
            auth = auth

          if ". Department" in auth:
            auth = auth.split('. Department')[0]
          elif ". Division" in auth:
            auth = auth.split('. Division')[0]
          else:
            auth = auth.split(',')[0]

          auth = auth.strip(' :')
          auth = scrtools.get_clean_author (auth)

          #eml = eml.replace('mailto:', '')
          eml = eml[::-1] #reverses the email string

          url = response.url


          l = ItemLoader(item=NcbiItem(), response=response)

          l.add_value('url', url)
          l.add_value('email', eml)
          l.add_value('authors', auth)
          l.add_value ('journal', GenNcbiSpider.journalName)
          l.add_value ('date',time.strftime("%d/%m/%Y"))
          return l.load_item()

   
    else: # DIV cor1

      print ('passed!!!..............................')

      auth = response.xpath('//div[@id="cor1"]/text()').extract_first()
      if auth:
        auth = auth.strip('* :')
        auth = auth.split(",")[0]
        auth = get_clean_author (auth)

      eml = response.xpath('//a[contains(@href, "mailto:")]/@data-email').extract_first()
      eml = eml[::-1] #reverses the email string

      if eml:
        url = response.url


        l = ItemLoader(item=NcbiItem(), response=response)

        l.add_value('url', url)
        l.add_value('email', eml)
        l.add_value('authors', auth)
        l.add_value ('journal', GenNcbiSpider.journalName)
        l.add_value ('date',time.strftime("%d/%m/%Y"))
        return l.load_item()

 #ENDOCRINOLOGY
  

  # journalName = "Experimental Diabetes Research" # Done        
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/144605/',
  #               'https://www.ncbi.nlm.nih.gov/pmc/issues/222634/'
  # ]

  # journalName = "Journal of Obesity" # Done
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/188854/',
  #               'https://www.ncbi.nlm.nih.gov/pmc/issues/248556/'
  # ]


  # journalName = "Journal of Nutrition and Metabolism" # Done
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/188853/',
  #               'https://www.ncbi.nlm.nih.gov/pmc/issues/249246/'
  # ]
  
  # journalName = "Diabetes and Metabolism" # Done
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/187476/',
  #               'https://www.ncbi.nlm.nih.gov/pmc/issues/195993/'
  # ]

  # journalName = "Journal of Diabetes Research" # Done
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/144605/',
  #               'https://www.ncbi.nlm.nih.gov/pmc/issues/222634/'
  # ]

  # journalName = "Vascular Health and Risk Management" # Done
  # start_urls = [
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/282182/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/263532/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/246883/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/231485/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/217742/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/204674/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/194155/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/185234/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/178371/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/168873/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/170273/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/170824/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/174332/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/175047/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/177648/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/175368/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/175367/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/163180/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/163093/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/163142/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/165139/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148898/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148900/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148899/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148901/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148894/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148895/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148896/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/148897/']

  # journalName = "International Journal of Endocrinology" # DOne
  # start_urls = [
  #   'https://www.ncbi.nlm.nih.gov/pmc/issues/233214/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/248033/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/264503/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/285776/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/182887/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/182886/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/194239/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/203489/',
  #    'https://www.ncbi.nlm.nih.gov/pmc/issues/218799/']


  # journalName = "Journal of Thyroid Research" # Done
  # start_urls = [
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/248349/',
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/264534/',
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/190748/',
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/191895/',
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/199258/',
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/219184/',
  #            'https://www.ncbi.nlm.nih.gov/pmc/issues/233340/']



  # journalName = "Journal of Osteoporosis" # DOne
  # start_urls = [
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/249293/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/264479/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/284340/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/190538/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/192865/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/206915/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/218827/',
  #             'https://www.ncbi.nlm.nih.gov/pmc/issues/235317/']


  # journalName = "Case Reports in Endocrinology" # Done
  # start_urls = [
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/284470/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/264527/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/248005/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/233327/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/218777/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/213085/',
  #                'https://www.ncbi.nlm.nih.gov/pmc/issues/213087/']

  # journalName = "European Thyroid Journal" # Done
  # start_urls = [


  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/268321/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/272770/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/278425/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/283357/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/252096/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/255969/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/260493/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/260586/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/263590/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/237067/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/240781/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/243743/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/245024/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/248615/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/229481/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/229482/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/229483/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/237581/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/233837/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/229478/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/229479/',
  #                  'https://www.ncbi.nlm.nih.gov/pmc/issues/229480/']






  #AGING

  # journalName = "Aging and Desiese"
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/206257/']

  # journalName = "Canadian Geriatrics Journal"
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/217031/']

#   journalName = "Clinical Interventions in Aging" #done
#   start_urls = [
#   'https://www.ncbi.nlm.nih.gov/pmc/issues/281800/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/262548/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/247059/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/230994/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/217746/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/204931/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/195435/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/184730/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178980/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/172022/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/172059/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178805/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178806/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178916/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178932/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178982/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/179048/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/178810/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/179423/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/179424/',
#    'https://www.ncbi.nlm.nih.gov/pmc/issues/179695/'
# ]

 #  journalName = "Current Gerontology and Geriatrics Research"
 #  start_urls = [
 #  'https://www.ncbi.nlm.nih.gov/pmc/issues/265071/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/254968/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/233368/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/218429/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/203488/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/196241/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/185387/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/178473/',
 # 'https://www.ncbi.nlm.nih.gov/pmc/issues/178352/']



  
  # journalName = "Journal of Aging Research"
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/191916/']

  # journalName = "Pathology of Aging and Age-related Decieses"
  # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/issues/223925/']

