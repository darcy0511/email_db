# -*- coding: utf-8 -*-
import scrapy
import subprocess
from email_db.items import ChinazWhoisDbItem
import re
import os

import sqlite3
import tldextract

domain_name_re = re.compile(r'Domain Name:\s?(.+)',re.IGNORECASE)
registrant_name_re = re.compile(r'Registrant Name:\s?(.+)',re.IGNORECASE)
registrant_organization_re = re.compile(r'Registrant Organization:\s?(.+)',re.IGNORECASE)
registrant_street_re = re.compile(r'Registrant Street:\s?(.+)',re.IGNORECASE)
registrant_city_re = re.compile(r'Registrant City:\s?(.+)',re.IGNORECASE)
registrant_state_re = re.compile(r'Registrant State/Province:\s?(.+)',re.IGNORECASE)
registrant_postal_re = re.compile(r'Registrant Postal Code:\s?(.+)',re.IGNORECASE)
registrant_country_re = re.compile(r'Registrant Country:\s?(.+)',re.IGNORECASE)

class ChinazWhoisSpider(scrapy.Spider):
    name = "chinaz_whois"
    allowed_domains = ["baidu.com"]
    start_urls = ['http://www.qq.com/']
    db_name = os.path.join(os.getcwd(),'email_data/email_db.db')
    item_tmp = ChinazWhoisDbItem.fields.keys()
    filepath = os.path.join(os.getcwd(),'email_data/reg_lower.csv')
    custom_settings = {"sqlite3_db":db_name,"fields_list":item_tmp}
    select_sql = 'select * from {table_name} where DOMAIN = ?;'.format(table_name=name)

    def __init__(self, filepath=None, minloc='0', maxloc='0', db_name=None, *args, **kwargs):
        super(ChinazWhoisSpider, self).__init__(*args, **kwargs)
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

                    p = subprocess.Popen(['whois', line], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    cfg = "file:"+os.path.join(os.getcwd(),"scrapy.cfg")
                    meta = {"num":num,'domain':line,'domain_data':p,'dont_obey_robotstxt':True,'dont_cache':True}
                    yield scrapy.Request("http://www.qq.com/", meta=meta,dont_filter=True ,callback=self.parse_whoischinaz)

    def parse_whoischinaz(self, response):
        p = response.meta['domain_data']
        r = p.communicate()[0]
        #p.kill()
	
        if domain_name_re.findall(r)==[] or domain_name_re.findall(r)==None:
            return

        item = ChinazWhoisDbItem()
        item["NUM"] = response.meta['num']
        item["DOMAIN"] = response.meta['domain']
        item['Registrant_Name'] = registrant_name_re.findall(r)[0] if registrant_name_re.findall(r)!=[] else ''
        item['Registrant_Organization'] = registrant_organization_re.findall(r)[0] if registrant_organization_re.findall(r)!=[] else ''
        item['Registrant_City'] = registrant_city_re.findall(r)[0] if registrant_city_re.findall(r)!=[] else ''
        item['Registrant_State'] = registrant_state_re.findall(r)[0] if registrant_state_re.findall(r)!=[] else ''
        item['Registrant_Country'] = registrant_country_re.findall(r)[0] if registrant_country_re.findall(r)!=[] else ''
        item['Registrant_Postal_Code'] = registrant_postal_re.findall(r)[0] if registrant_postal_re.findall(r)!=[] else ''
        item['Registrant_Street'] = registrant_street_re.findall(r)[0] if registrant_street_re.findall(r)!=[] else ''

        return item          
