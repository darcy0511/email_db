# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EmailDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NUM = scrapy.Field()
    DNS = scrapy.Field()
    MX = scrapy.Field()
    SHORTNAME = scrapy.Field()
    INFO = scrapy.Field()

class ChinazDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NUM = scrapy.Field()
    DOMAIN = scrapy.Field()
    SPONSOR = scrapy.Field()
    SPONSOR_NATURE = scrapy.Field()
    DOMAIN_NAME = scrapy.Field()
    SPONSOR_TIME = scrapy.Field()
    Registrar = scrapy.Field()
    Registrant_Organization = scrapy.Field()
    Updated_Date = scrapy.Field()
    Registrar_WHOIS_Server = scrapy.Field()
    KEY_Title = scrapy.Field()
    KEY_KeyWords = scrapy.Field()
    KEY_Description = scrapy.Field()
    Registrant_City = scrapy.Field()
    Registrant_State = scrapy.Field()
    Registrant_Postal_Code = scrapy.Field()
    Registrant_Country = scrapy.Field()

class ChinazIcpDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NUM = scrapy.Field()
    DOMAIN = scrapy.Field()
    SPONSOR = scrapy.Field()
    SPONSOR_NATURE = scrapy.Field()
    DOMAIN_NAME = scrapy.Field()
    SPONSOR_TIME = scrapy.Field()

class ChinazKeyDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NUM = scrapy.Field()
    DOMAIN = scrapy.Field()
    KEY_Title = scrapy.Field()
    KEY_KeyWords = scrapy.Field()
    KEY_Description = scrapy.Field()

class ChinazWhoisDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NUM = scrapy.Field()
    DOMAIN = scrapy.Field()
    Registrant_Name = scrapy.Field()
    Registrant_Organization = scrapy.Field()
    Registrant_City = scrapy.Field()
    Registrant_State = scrapy.Field()
    Registrant_Country = scrapy.Field()
    Registrant_Postal_Code = scrapy.Field()
    Registrant_Street = scrapy.Field()

	
class ChinazSeoDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NUM = scrapy.Field()
    DOMAIN = scrapy.Field()
    SPONSOR = scrapy.Field()
    SPONSOR_NATURE = scrapy.Field()
    SPONSOR_TIME = scrapy.Field()
    KEY_Title = scrapy.Field()
    KEY_KeyWords = scrapy.Field()
    KEY_Description = scrapy.Field()
