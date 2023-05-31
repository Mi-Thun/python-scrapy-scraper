import scrapy
import json
from ..items import DatacampItem

with open('catagory.json') as file:
    catagory_json = json.load(file)

with open('keyword.json') as file:
    keyword_json = json.load(file)

class DatacampSpiderSpider(scrapy.Spider):
    name = "datacamp_spider"
    allowed_domains = ["datacamp.com"]
    start_urls = ['https://www.datacamp.com/']

    def start_requests(self):
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
            keyword = keyword.split()
            if len(keyword) == 2:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0]) +'%20' + str(keyword[1])
                yield scrapy.Request(search_url, callback=self.parse_search_result, meta={'keyword': keyword, 'page': search_url})
            elif len(keyword) == 3:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0]) +'%20' + str(keyword[1]) + '%20' + str(keyword[2])
                yield scrapy.Request(search_url, callback=self.parse_search_result, meta={'keyword': keyword, 'page': search_url})
            elif len(keyword) == 4:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0]) +'%20' + str(keyword[1]) + '%20' + str(keyword[2]) + '%20' + str(keyword[3])
                yield scrapy.Request(search_url, callback=self.parse_search_result, meta={'keyword': keyword, 'page': search_url})
            else:
                search_url = 'https://www.datacamp.com/search?q=' + str(keyword[0])
                yield scrapy.Request(search_url, callback=self.parse_search_result, meta={'keyword': keyword, 'page': search_url})
            
    def parse_search_result(self, response):
        next_page = response.css('a.js-load::attr(href)').get()
        if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse_search_result, meta=response.meta)
        
        for i in response.css('.ds-snowplow-search-v2-result-course'):
            single_course_url = i.css('a.ds-snowplow-search-v2-result-course::attr(href)').get()
            product_url = 'https://www.datacamp.com' + str(single_course_url)
            yield response.follow(product_url, callback= self.parse_product_page, meta={'product_url': product_url})

    def parse_product_page(self, response):
        items = DatacampItem()
        
        url = response.meta['product_url']
        xpath_expression = f'//script[@id="{url}"]/text()'
        script_content = response.xpath(xpath_expression).get()

        if script_content:
            script_content = script_content.strip()
            try:
                data = json.loads(script_content)
                availableLanguage = data['availableLanguage']
                skill = data.get('about', [])
                Learning_Product_Image_URL = data.get('image', '')
                syllabus_sections = data.get('syllabusSections', [])
                syllabus_names = [section['name'] for section in syllabus_sections]
                module_description = [module['description'] for module in syllabus_sections]

            except json.JSONDecodeError:
                pass
        
        xpath_expression2 = f'//script[@id="__NEXT_DATA__"]/text()'
        xpath_expression2 = response.xpath(xpath_expression2).get()

        if xpath_expression2:
            xpath_expression2 = xpath_expression2.strip()
            try:
                data = json.loads(xpath_expression2)
                chapters = data['props']['pageProps']['course']['chapters']
                level = data['props']['pageProps']['course']
                exercise_details = []
                for chapter in chapters:
                    exercises = chapter['exercises']
                    single_ex = []
                    for exercise in exercises:
                        if exercise['title'] != None:
                            if exercise['type'] == 'VideoExercise':
                                just_type = 'Video'
                            elif exercise['type'] == 'PureMultipleChoiceExercise':
                                just_type = 'Multiple Choice Questions'
                            else:
                                just_type = 'Exercise'
                                
                            single_ex.append({
                                'Lesson Name': exercise['title'],
                                "Lesson Description": None,
                                "Type": just_type,
                                'Raw Type': exercise['type'],
                                'time': None
                            })
                    difficultyLevel = level['difficultyLevel']
                    exercise_details.append(single_ex)
                    single_ex = []
                    
            except json.JSONDecodeError:
                pass

        if len(response.css('.css-1ton54v-CoursePage::text')) >= 4:
            enrolled = response.css('.css-1ton54v-CoursePage::text')[3].get()
        else:
            enrolled = None
            
        items['Learning_Product_Name'] = response.css('.css-1r7eu3v-CoursePage::text').get()
        
        catagoryfromall = []
        for ii in catagory_json:
            for valye1 in ii.values():
                for kk in valye1:
                    if kk == url:
                        catagoryfromall.extend(ii.keys())
        items['Learning_Product_Category'] = catagoryfromall
        
        items['Learning_Product_Image_URL'] = Learning_Product_Image_URL[0]
        items['Learning_Product_URL'] = response.meta['product_url']
        items['Learning_Product_Price'] = None

        topic = []
        for syllabus in syllabus_names:
            topic.append({'Topic Name': syllabus})
        items['Topics'] = topic
        
        keywordfromall = []
        for iii in keyword_json:
            for valye2 in iii.values():
                for kkk in valye2:
                    if kkk == url:
                        keywordfromall.extend(iii.keys())
        items['Keyword_Matches'] = keywordfromall
        
        items['Vendor'] = "Datacamp"
        
        skil = []
        for sk in skill:
            skil.append({'Skill Name': sk})
        items['Skills'] = skil    
            
        items['Level'] = int(difficultyLevel)
        items['Total_Time'] = response.css('.css-1ton54v-CoursePage::text')[0].get()
        items['Provided_by'] = response.css('.css-2ce4tz-InstructorDetails::text').get()
        items['Related_Job_Titles'] = []
        if availableLanguage[0] == 'en':
            language = 'English'
        items['Language'] = language
        items['Type'] = "Course"
        items['Short_Description'] = response.css('.css-1n2d7d8-CoursePage::text').get()
        items['Long_Description'] = response.css('.css-bqmo1r-CourseDetails::text').get()
        items['Prerequisites'] = response.css('.css-b7klgb-CourseDetails~ .css-b7klgb-CourseDetails+ .css-b7klgb-CourseDetails .css-13nwhvi-CourseDetails::text').getall()
        items['UserRating'] = response.css('.css-179yjzv-CoursePage::text').get()
        items['UserRatingCount'] = response.css('.css-15rqx78-CoursePage::text').get()
        
        modules = []
        for k in range(len(syllabus_names)):
            module = {
                'Module Name': syllabus_names[k],
                'Module Description': module_description[k],
                'Time': None,
                'Lessons': exercise_details[k]
            } 
            modules.append(module)
        items['Modules'] = modules
        
        items['Enrolled'] = enrolled

        yield items
    