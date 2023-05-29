# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DatacampItem(scrapy.Item):
    # define the fields for your item here like:
    Learning_Product_Name = scrapy.Field()
    Learning_Product_Category = scrapy.Field()
    Learning_Product_Image_URL = scrapy.Field()
    Learning_Product_URL = scrapy.Field()
    Learning_Product_Price = scrapy.Field()
    Topics = scrapy.Field()
    Keyword_Matches = scrapy.Field()
    Vendor = scrapy.Field()
    Skills = scrapy.Field()
    Level = scrapy.Field()
    Total_Time = scrapy.Field()
    Provided_by = scrapy.Field()
    Related_Job_Titles = scrapy.Field()
    Language = scrapy.Field()
    Type = scrapy.Field()
    Short_Description = scrapy.Field()
    Long_Description = scrapy.Field()
    Prerequisites = scrapy.Field()
    UserRating = scrapy.Field()
    UserRatingCount = scrapy.Field()
    Modules = scrapy.Field()
    Enrolled = scrapy.Field()
    available_language = scrapy.Field()
