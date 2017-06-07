# -*- coding: utf-8 -*-
import scrapy, re, time#, html

from scrtools import *

from scrapy.loader import ItemLoader
from sciencedirect.items import SciencedirectItem
from urllib import parse

class GenericSciencedirectSpider(scrapy.Spider):
  name = "gen_scidir"
  allowed_domains = ["www.sciencedirect.com"]


  #IMMUNOLOGY

  # start_urls = ['http://www.sciencedirect.com/science/journal/10747613/44/6'] 
  # journalName = 'Immunity' # TO PROCESS SCRAPS THROUGH SPLASH

  # start_urls = ['http://www.sciencedirect.com/science/journal/14714906/24/1'] 
  # journalName = 'Trends in Immunology' # Done

  # start_urls = ['http://www.sciencedirect.com/science/journal/00916749/111/1'] 
  # journalName = 'Journal of Allergy and Clinical Immunology'  # SPLASH?

  # start_urls = ['http://www.sciencedirect.com/science/journal/09527915/15/1'] 
  # journalName = 'Current Opinion in Immunology' # DONE

  # start_urls = ['http://www.sciencedirect.com/science/journal/23523018/1/1'] 
  # journalName = 'The Lancet HIV' #Done

  # start_urls = ['http://www.sciencedirect.com/science/journal/10445323/15/1'] 
  # journalName = 'Seminars in Immunology' #DONE

  # start_urls = ['http://www.sciencedirect.com/science/bookseries/00652776/81'] 
  # journalName = 'Advances in Immunology' #DONE

  # start_urls = ['http://www.sciencedirect.com/science/journal/08891591/17/1'] 
  # journalName = 'Brain, Behavior, and Immunity' #DONE

  # start_urls = ['http://www.sciencedirect.com/science/journal/15689972/1/1-2'] 
  # journalName = 'Autoimmunity Reviews' #Done

  #start_urls = ['http://www.sciencedirect.com/science/journal/15216616/106/1'] 
  #journalName = 'Clinical Immunology' 

  start_urls = ['http://www.sciencedirect.com/science/journal/10510443/1/1'] 
  journalName = 'Journal of Vascular and Interventional Radiology' 

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 




  def parse(self,response):
    toc_urls = response.xpath('//a[contains(@class, "cLink artTitle")]/@href').extract()
    for url in toc_urls:
      yield scrapy.Request (response.urljoin(url), callback=self.parse_site_data)
      

    next_page =  response.xpath('//a[contains(@title, "Next volume/issue")]/@href').extract_first()
    
    if next_page is not None:
      next_page = response.urljoin(next_page)
      yield scrapy.Request(response.urljoin(next_page), callback=self.parse)



  def parse_site_data (self, response):

    li_tags = response.xpath('//ul[@class="authorGroup noCollab svAuthor"]/li')

    for li_elm in li_tags:
      eml = li_elm.xpath('a[@class="auth_mail"]/@href').extract_first()

      if eml:

        eml = eml.replace('mailto:', '')
        eml = eml.strip('\t\n\r ')
        
        auth = li_elm.xpath('a[@class="authorName svAuthor"]/text()').extract_first()
        #auth = html.unescape(auth)
        auth = get_clean_author(auth)


        url = response.url


        l = ItemLoader(item=SciencedirectItem(), response=response)

        l.add_value('url', url)
        l.add_value('email', eml)
        l.add_value('authors', auth)
        l.add_value ('journal', GenericSciencedirectSpider.journalName)
        l.add_value ('date',time.strftime("%d/%m/%Y"))
        return l.load_item()




  #ENDOCRINOLOGY

  # start_urls = ['http://www.sciencedirect.com/science/journal/10568727/30/8'] #DONE
  # journalName = 'Journal of Diabetes and its Complications' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/08898529/32/1'] #Done
  # journalName = 'Endocrinology and Metabolism Clinics of North America' 
 
  # start_urls = ['http://www.sciencedirect.com/science/journal/09394753/13/1'] # Done
  # journalName = 'Nutrition, Metabolism and Cardiovascular Diseases' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/10967192/78/1'] # Done
  # journalName = 'Molecular Genetics and Metabolism' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/22144269/1'] # Done
  # journalName = 'Molecular Genetics and Metabolism Reports' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/12623636/29/1']  # Done
  # journalName = 'Diabetes & Metabolism' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/09600760/84/1']  # Done
  # journalName = 'The Journal of Steroid Biochemistry and Molecular Biology' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/01688227/59/1'] # Done
  # journalName = 'Diabetes Research and Clinical Practice' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/22140301/1']  # DONE
  # journalName = 'Metabolic Engineering Communications' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/02715317/23/1'] # Done
  # journalName = 'Nutrition Research' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/14243903/3/1'] # Done
  # journalName = 'Pancreatology' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/08999007/19/1'] # Done
  # journalName = 'Nutrition' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/17519918/1/1'] # Done
  # journalName = 'Primary Care Diabetes' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/10946950/6/1']  # Done
  # journalName = 'Journal of Clinical Densitometry' 


  # start_urls = ['http://www.sciencedirect.com/science/journal/14992671/30/1'] # Done
  # journalName = 'Canadian Journal of Diabetes' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/1871403X/1/1'] 
  # journalName = 'Obesity Research & Clinical Practice' # Done


  # start_urls = ['http://www.sciencedirect.com/science/journal/10966374/13/1'] 
  # journalName = 'Growth Hormone & IGF Research' # Done

  # start_urls = ['http://www.sciencedirect.com/science/journal/18714021/1/1'] 
  # journalName = 'Diabetes & Metabolic Syndrome: Clinical Research & Reviews' # Done

  # start_urls = ['http://www.sciencedirect.com/science/journal/22146237/1/1'] 
  # journalName = 'Journal of Clinical & Translational Endocrinology'  # Done

  # start_urls = ['http://www.sciencedirect.com/science/journal/00034266/65/1'] #  Done
  # journalName = 'Annales dEndocrinologie' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/15750922/50/1'] # Done
  # journalName = 'Endocrinología y Nutrición' 

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

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 

  # start_urls = [''] 
  # journalName = '' 




  #AGING

  # start_urls = ['http://www.sciencedirect.com/science/journal/15681637/1/1'] 
  # journalName = 'Ageing Research Reviews' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/01974580/24/1'] 
  # journalName = 'Neurobiology of Aging' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/00476374/124/1'] 
  # journalName = 'Mechanisms of Ageing and Development' 


  # start_urls = ['http://www.sciencedirect.com/science/journal/05315565/38/1-2'] 
  # journalName = 'Experimental Gerontology' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/01674943/36/1'] 
  # journalName = 'Archives of Gerontology and Geriatrics' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/22105220/1/1'] 
  # journalName = 'Biomedicine & Aging Pathology' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/08904065/17/1'] 
  # journalName = 'Journal of Aging Studies' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/18739598/1/1'] 
  # journalName = 'International Journal of Gerontology' 

  # start_urls = ['http://www.sciencedirect.com/science/journal/22108335/1/1'] 
  # journalName = 'Journal of Clinical Gerontology and Geriatrics' 



  #PHARMACOLOGY

  # start_urls = ['http://www.sciencedirect.com/science/journal/01637258/97/1'] 
  # journalName = 'Pharmacology & Therapeutics'

  # start_urls = ['http://www.sciencedirect.com/science/journal/01656147/24/1'] 
  # journalName = 'Trends in Pharmacological Sciences'
  
  # start_urls = ['http://www.sciencedirect.com/science/journal/10745521/10/1'] #1
  # journalName = 'Chemistry & Biology'

  # start_urls = ['http://www.sciencedirect.com/science/journal/03043959/101/1-2'] #1
  # journalName = 'Pain'

  # start_urls = ['http://www.sciencedirect.com/science/journal/00062952/65/1'] #1
  # journalName = 'Biochemical Pharmacology'

  # start_urls = ['http://www.sciencedirect.com/science/journal/14714892/3/1'] #1
  # journalName = 'Current Opinion in Pharmacology'

  # start_urls = ['http://www.sciencedirect.com/science/journal/13596446/8/1'] #1
  # journalName = 'Drug Discovery Today'

  # start_urls = ['http://www.sciencedirect.com/science/journal/01663542/57/1-2'] #1
  # journalName = 'Antiviral Research'

  # start_urls = ['http://www.sciencedirect.com/science/journal/0924977X/13/1'] #1
  # journalName = 'European Neuropsychopharmacology'

  # start_urls = ['http://www.sciencedirect.com/science/journal/13687646/6/1'] #1
  # journalName = 'Drug Resistance Updates'

  # start_urls = ['http://www.sciencedirect.com/science/journal/10436618/47/1'] #1
  # journalName = 'Pharmacological Research'
