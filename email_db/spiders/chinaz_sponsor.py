# -*- coding: utf-8 -*-
import scrapy
from email_db.items import ChinazIcpDbItem 
import traceback
import os

import sqlite3
import tldextract 


class ChinazSponsorSpider(scrapy.Spider):
    name = "chinaz_sponsor"
    #allowed_domains = ["http://icp.chinaz.com/"]
    start_urls = ['http://icp.chinaz.com/']

    db_name = os.path.join(os.getcwd(),'email_data/email_db.db')
    item_tmp = ChinazIcpDbItem.fields.keys()
    filepath = os.path.join(os.getcwd(),'email_data/reg_lower.csv')
    custom_settings = {"sqlite3_db":db_name,"fields_list":item_tmp}
    select_sql = 'select * from {table_name} where DOMAIN = ?;'.format(table_name=name)


    def __init__(self, filepath=None, minloc='0', maxloc='0', db_name=None, *args, **kwargs):
        super(ChinazSponsorSpider, self).__init__(*args, **kwargs)
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

                    item = ChinazIcpDbItem()
                    #self.logger.info('Parse function called on {domain} of {num}'.format(domain=item['DOMAIN'],num=item["NUM"]))
                    url_search = 'http://icp.chinaz.com/?s={domain}'.format(domain=line)
                    yield scrapy.Request(url_search, meta={"num":num,'domain':line} ,callback=self.parse_icpchinaz)

    def parse_icpchinaz(self, response):
        selector = scrapy.Selector(response=response)

        sp_list = selector.xpath('//li[@class="bg-gray clearfix"]/p/text()').extract()
        sn_list = selector.xpath('//strong[@class="fl fwnone"]/text()').extract()
        st_list = selector.xpath('//li[@class="clearfix"]/p/text()').extract()
        try:
            SPONSOR = sp_list[0]
            SPONSOR_NATURE = sn_list[0]
            DOMAIN_NAME = st_list[0]
            SPONSOR_TIME = st_list[1]
        except Exception,e:
            #self.logger.warning(response.meta['domain']+"->"+e)
            #traceback.print_exc()
            return

        item = ChinazIcpDbItem()
        item["NUM"] = response.meta['num']
        item["DOMAIN"] = response.meta['domain']
        item['SPONSOR'] = SPONSOR
        item['SPONSOR_NATURE'] = SPONSOR_NATURE 
        item['DOMAIN_NAME'] = DOMAIN_NAME 
        item['SPONSOR_TIME'] = SPONSOR_TIME 
        return item 

