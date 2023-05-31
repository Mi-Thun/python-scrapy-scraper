import scrapy
import json

key_and_keyword = []
key_and_category = []

class DatacampSpiderSpider(scrapy.Spider):
    name = "datacamp_catagory_keyword"
    allowed_domains = ["datacamp.com"]
    start_urls = ['https://www.datacamp.com/']

    def start_requests(self):
        catagory_list = ['Computer Science', 'Mathematics', 'Business', 'Engineering', 'Data and Science', 
                         'Programming', ' Information Security', ]
        
        keyword_list = ['Artificial Intelligence', 'Algorithms', 'Data Structures', 'Internet of Things', 
                        'Information Technology', 'Computer Networking', 'Machine Learning', 'DevOps', 
                        'Deep Learning', 'Natural Language Processing', 'Cryptography', 'Quantum Computing',
                        'Human-Computer Interaction (HCI)', 'Distributed Systems', 'Blockchain Development',
                        'Nutrition', 'Wellness', 'Public Health', 'Health Care', 'Nursing', 'Anatomy', 
                        'Veterinary Science', 'Continuing Medical Education (CME)', 'Statistics', 'Probability',
                        'Foundations of Mathematics', 'Calculus', 'Algebra & Geometry', 'Discrete Mathematics',
                        'Trigonometry', 'Geometry', 'Algebra', 'Management', 'Tax Preparation', 'Business Writing',
                        'Technical Writing', 'Leadership', 'Entrepreneurship', 'Marketing',
                        'Strategic Management', 'Business Intelligence', 'Accounting', 'Human Resources',
                        'Project Management', 'Sales', 'Design Thinking', 'Business Software',
                        'Risk Management', 'Corporate Social Responsibility', 'Customer Service', 'Nonprofit Management',
                        'Autocad', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
                        'Robotics', 'Nanotechnology', 'GIS', 'Textiles', 'Manufacturing', 'BIM',
                        'CAD', 'Chemical Engineering', 'Energy Systems', 'Bioinformatics', 'Big Data', 'Data Mining',
                        'Data Analysis', 'Data Visualization', 'Google Data Analytics', 'Data Analytics',
                        'Mobile Development', 'Web Development', 'Databases', 'Game Development',
                        'Programming Languages', 'Software Development', 'Cloud Computing', 'Communication Skills',
                        'Career Development', 'Self Improvement', 'Presentation Skills', 'Cybersecurity',
                        'Network Security', 'Ethical Hacking', 'Digital Forensics', 'Penetration Testing',
                        'Malware Analysis', 'DevSecOps', 'Open Source Intelligence', 'Threat intelligence']
        
        for keyword in keyword_list:
            key_js = keyword
            keyword = keyword.split()
            if len(keyword) == 2:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0]) +'%20' + str(keyword[1])
                yield scrapy.Request(search_url, callback=self.parse_keyword_search_result, meta={'keyword': keyword, 'page': search_url, 'key_js': key_js})
            elif len(keyword) == 3:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0]) +'%20' + str(keyword[1]) + '%20' + str(keyword[2])
                yield scrapy.Request(search_url, callback=self.parse_keyword_search_result, meta={'keyword': keyword, 'page': search_url, 'key_js': key_js})
            elif len(keyword) == 4:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0]) +'%20' + str(keyword[1]) + '%20' + str(keyword[2]) + '%20' + str(keyword[3])
                yield scrapy.Request(search_url, callback=self.parse_keyword_search_result, meta={'keyword': keyword, 'page': search_url, 'key_js': key_js})
            else:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0])
                yield scrapy.Request(search_url, callback=self.parse_keyword_search_result, meta={'keyword': keyword, 'page': search_url, 'key_js': key_js})
                
        for catagory in catagory_list:
            cata_js = catagory
            catagory = catagory.split()
            if len(catagory) == 2:
                search_url = 'https://www.datacamp.com/search?q=' + str(catagory[0]) +'%20' + str(catagory[1])
                yield scrapy.Request(search_url, callback=self.parse_catagory_search_result, meta={'catagory': catagory, 'page': search_url, 'cata_js': cata_js})
            elif len(catagory) == 3:
                search_url = 'https://www.datacamp.com/search?q=' + str(catagory[0]) +'%20' + str(catagory[1]) + '%20' + str(catagory[2])
                yield scrapy.Request(search_url, callback=self.parse_catagory_search_result, meta={'catagory': catagory, 'page': search_url, 'cata_js': cata_js})
            else:
                search_url = 'https://www.datacamp.com/search?q=' + str(catagory[0])
                yield scrapy.Request(search_url, callback=self.parse_catagory_search_result, meta={'catagory': catagory, 'page': search_url, 'cata_js': cata_js})
            
    def parse_keyword_search_result(self, response):
        single_keyword = []
        next_page = response.css('a.js-load::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse_keyword_search_result, meta=response.meta)
        # count = 1
        for i in response.css('.ds-snowplow-search-v2-result-course'):
            # count = count + 1
            single_course_url = i.css('a.ds-snowplow-search-v2-result-course::attr(href)').get()
            product_url = 'https://www.datacamp.com' + str(single_course_url)
            single_keyword.append(product_url)
            # if count > 3:
            #     break
            
        new_dict = {str(response.meta['key_js']): single_keyword}
        key_and_keyword.append(new_dict)
            
    def parse_catagory_search_result(self, response):
        single_catagory = []
        next_page = response.css('a.js-load::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse_catagory_search_result, meta=response.meta)
        # count = 1
        for i in response.css('.ds-snowplow-search-v2-result-course'):
            # count = count + 1
            single_course_url = i.css('a.ds-snowplow-search-v2-result-course::attr(href)').get()
            product_url = 'https://www.datacamp.com' + str(single_course_url)
            single_catagory.append(product_url)
            # if count > 3:
            #     break
    
        new_dict = {str(response.meta['cata_js']): single_catagory}
        key_and_category.append(new_dict)
        
    def closed(self, reason):
        key_and_keyword_json = json.dumps(key_and_keyword)
        key_and_category_json = json.dumps(key_and_category)
        
        file_path_catagory = 'catagory.json'
        with open(file_path_catagory, 'w') as file:
            file.write(key_and_category_json)
            
        file_path_keyword = 'keyword.json'
        with open(file_path_keyword, 'w') as file:
            file.write(key_and_keyword_json)


