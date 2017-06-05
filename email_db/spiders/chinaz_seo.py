# -*- coding: utf-8 -*-
import scrapy
from email_db.items import ChinazSeoDbItem 
import traceback
import os

import sqlite3
import tldextract 

class ChinazSeoSpider(scrapy.Spider):
    name = "chinaz_seo"
    #allowed_domains = ["http://icp.chinaz.com/"]
    start_urls = ['http://seo.chinaz.com/']

    db_name = os.path.join(os.getcwd(),'email_data/email_db.db')
    item_tmp = ChinazSeoDbItem.fields.keys()
    filepath = os.path.join(os.getcwd(),'email_data/reg_lower.csv')
    custom_settings = {"sqlite3_db":db_name,"fields_list":item_tmp}
    select_sql = 'select * from {table_name} where DOMAIN = ?;'.format(table_name=name)

	
    def __init__(self, filepath=None, minloc='0', maxloc='0', db_name=None, *args, **kwargs):
        super(ChinazSeoSpider, self).__init__(*args, **kwargs)
        if filepath != None: self.filepath = filepath
        if db_name != None: self.db_name = db_name
        self.maxloc = int(maxloc)
        self.minloc = int(minloc)

    def parse(self, response):
        with open(self.filepath,'rU') as f, sqlite3.connect(self.db_name) as conn:
            for num, line in enumerate(f):
                if num >= self.minloc and num <= self.maxloc:
                    line = line.replace(' ','').replace("\n","")
                    if line.find('.') == -1:
                        continue
                    line = tldextract.extract(line).registered_domain
                    print line
                    if conn.execute(self.select_sql,(line,)).fetchone() != None:
                        #print '------------continue-----------'
                        continue

                    #self.logger.info('Parse function called on {domain} of {num}'.format(domain=item['DOMAIN'],num=item["NUM"]))
                    url_search = 'http://seo.chinaz.com/{domain}'.format(domain=line)
                    yield scrapy.Request(url_search, meta={"num":num,'domain':line} ,callback=self.parse_seochinaz)

    def parse_seochinaz(self, response):
        selector = scrapy.Selector(response=response)
        
        sn_list = selector.xpath('//*[@id="seoinfo"]/div/ul/li[5]/div[2]/div[2]/strong/text()').extract()
        sp_list = selector.xpath('//*[@id="seoinfo"]/div/ul/li[5]/div[2]/div[3]/strong/text()').extract()
        st_list = selector.xpath('//*[@id="seoinfo"]/div/ul/li[5]/div[2]/div[4]/strong/text()').extract()

        try:
            SPONSOR = sp_list[0]
            SPONSOR_NATURE = sn_list[0]
            SPONSOR_TIME = st_list[0]
        except Exception,e:
            #self.logger.warning(response.meta['domain']+"->"+e)
            #traceback.print_exc()
            return

        key_list = selector.xpath('//td[@class="w61-0"]/div[@class="ball"]/text()').extract()
		
        item = ChinazSeoDbItem()
        item["NUM"] = response.meta['num']
        item["DOMAIN"] = response.meta['domain']
        item['SPONSOR'] = SPONSOR
        item['SPONSOR_NATURE'] = SPONSOR_NATURE 
        item['SPONSOR_TIME'] = SPONSOR_TIME 
        item['KEY_Title'] = key_list[0]
        item['KEY_KeyWords'] = key_list[1]
        item['KEY_Description'] = key_list[2]
        return item 

