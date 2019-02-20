from selenium import webdriver
from bs4 import BeautifulStoneSoup

class Scraper:
	
	def __init__(self):
		self.platform = 'Crowdfunder'
		
	
	def start_browser(self,browser,driver_binary):
		if browser=='Safari':
			browser = webdriver.Safari(executable_path=driver_binary);
		elif browser=='Firefox':
			browser = webdriver.Firefox(executable_path=driver_binary);
		elif browser=='Chrome':
			browser = webdriver.Chrome(executable_path=driver_binary);
		else:
			print('Not a valid option! Browser not recognized or supported!')
		return browser
	
	'''
	def get_project_categories(projects_url):
		
		browser.get(projects_url)
		
		# Find the category dropdown menu
		dropdown_menu = browser.find_element_by_class_name('cf-select__trigger')
		#dropdown_menu.click()

		# Get a list of the categories and navigate to the second one
		category_selector = browser.find_element_by_class_name('cf-select__dropdown')
		category_obj = category_selector.find_elements_by_tag_name('li')
		category_list = [category.text.replace(' ','+') for category in category_obj]
		del category_list[:1]
		
		return category_list
		
	def get_category_url(category,campaign_state=None):
		
		if campaign_state is None:
			return 'https://www.crowdfunder.co.uk/search/projects?filter[c]='+category.replace(' ','+')
		
		elif campaign_state =='recent':
			return 'https://www.crowdfunder.co.uk/search/projects?filter[c]='+category.replace(' ','+')+'&filter[t]=recent&filter[s]='
		
		elif campaign_state =='pending':
			return 'https://www.crowdfunder.co.uk/search/projects?filter[c]='+category.replace(' ','+')+'&filter[t]=pending&filter[s]='
		
		elif campaign_state =='ending':
			return 'https://www.crowdfunder.co.uk/search/projects?filter[c]='+category.replace(' ','+')+'&filter[t]=ending&filter[s]='
		
		elif campaign_state =='successful':
			return 'https://www.crowdfunder.co.uk/search/projects?filter[c]='+category.replace(' ','+')+'&filter[t]=successful&filter[s]='
		
		elif campaign_state =='overfunding':
			return 'https://www.crowdfunder.co.uk/search/projects?filter[c]='+category.replace(' ','+')+'&filter[t]=overfunding&filter[s]='
		
		else:
			print('Not a valid option')
			exit()
	
	def get_category_page_url(category,campaign_state,page):
		get_category_url(category,campaign_state)+'&page='+str(page)
		
		return category_page_url

	def pages_in_category(category,campaign_state):
		
		browser.get(get_category_url(category,campaign_state));
		pagination = browser.find_elements_by_css_selector('a.cf-button.cf-button--pagination')
		page_numbers = [page.text for page in pagination]

		if len(page_numbers)!= 0:
			return int(page_numbers[-1])
		else:
			return 1
	'''






	