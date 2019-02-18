# cwdprophet
# Created by Jorge Alejandro Preciado Lopez on 2019-02-17.

from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Campaign:
	'''
	Attributes:
	'''
	
	def __init__(self,campaign_url=None):
		self.campaign_url = campaign_url
		browser = start_browser('Safari','/usr/bin/safaridriver')
		browser.get(self.campaign_url)
		self.soup = BeautifulSoup(browser.page_source,'html.parser')
		browser.quit()
		
	
	def copy(self):
		"""
		Return a copy of the Campaign object.
		Args:
			
		Returns:
			(Campaign): copy of the Campaign object.
		"""
		return Campaign(self.campaign_url)
	
	
	def creator(self):
		creator = self.soup.find('a',{'class':'cf-anchor cf-anchor--light-underline'}).text
		
		return creator
	

	def location(self):
		return self.soup.find('a',{'class':'cf-anchor cf-anchor--light-underline','rel':'nofollow'}).text
	
	
	def deadline(self):
		
		report = self.soup.find('span',{'class':'cf-text--thick'}).text
		day, month, year = report.split()[1:4]
		date = ' '.join([day,month,year])
		
		return date
	
	
	def duration(self):
		
		report = self.soup.find('span',{'class':'cf-text--thick'}).text
		duration = report.split()[-2]
		return duration
	
	
	def fbpage(self):
		
		a_class = 'cf-share__button cf-share__button--small cf-share__button--expanded cf-share__button--facebook';
		
		if self.soup.find('a',{'class':a_class})==None:
				project_fb = None
		else:
			project_fb = self.soup.find('a',{'class':a_class})['href']
			
		return project_fb
	
	
	def twpage(self):
		
		a_class = 'cf-share__button cf-share__button--small cf-share__button--expanded cf-share__button--twitter';
			
		if self.soup.find('a',{'class':a_class})==None:
			project_tw = None
		else:
			project_tw = self.soup.find('a',a_class)['href']
			
		return project_tw
	
	
	def Nupdates(self):
		campaign_tabs = self.soup.find_all('span',{'class':'cf-badge cf-badge--dim'})
		Nupdates = int(campaign_tabs[0].string)
		
		return Nupdates


	def Ncomments(self):
		campaign_tabs = self.soup.find_all('span',{'class':'cf-badge cf-badge--dim'})
		Ncomments = int(campaign_tabs[1].string)
		
		return Ncomments


	def Ninvestors(self):
		campaign_tabs = self.soup.find_all('span',{'class':'cf-badge cf-badge--dim'})
		Ninvestors = int(campaign_tabs[2].string)
	
		return Ninvestors
	
	def pledges(self):
		
		browser = start_browser('Safari','/usr/bin/safaridriver')
		browser.get(self.campaign_url+'/backers')
		
		pledges = []
		dates = []
		names = []
		more_supporters = True
		
		while more_supporters==True:
			print('Scraping:',browser.current_url)
			time.sleep(3)
			soup = BeautifulSoup(browser.page_source,'html.parser')

			tags = soup.find_all('article',{'class':'cf-well', 'data-well':'plain', 'data-well-spacing':'vertical'})

			for tag in tags:
				#print(tag.find("span", class_="cf-text--light").string.split()[-1][1:])
				pledges.append(float(tag.find("span", class_="cf-text--light").string.split()[-1][1:].replace(',','')))

			for tag in tags:
				#print(tag.find("p", class_="cf-text").string)
				dates.append(tag.find("p", class_="cf-text").string)

			for tag in tags:
				#print(tag.find("a"))
				if tag.find("a")==None:
					names.append('Anonymous')
				else:
					names.append(tag.find("a").string)

			button = soup.find('a',{'class':'cf-button cf-button--small cf-button--hollow', 'data-icon-button':'next'})

			if button is None:
				more_supporters = False;
			if button is not None:
				browser.get(self.campaign_url+'/backers'+button['href'])
		
		browser.quit()
		
		return pledges[::-1], dates[::-1], names[::-1]
	
	
	def report(self):
		print('URL:',self.campaign_url)
		print('Creator:',self.creator())
		print('Location:',self.location())
		print('Deadline:',self.deadline())
		print('Duration:',self.duration(),'days')
		print('Project FB:',self.fbpage())
		print('Project TWitter:',self.twpage())
		print('Nupdates:',self.Nupdates())
		print('Ncomments:',self.Ncomments())
		print('Ninvestors:',self.Ninvestors())
		
	

def load_campaign(campaign_url,display=False):
	
	"""
	Load a Crowdfunder campaign from a URL.
	Args:
		campaign_url (str): URL of the campaign
	Returns:
		(Campaign): loaded Campaign object
	"""
	
	#browser = start_browser('Safari','/usr/bin/safaridriver')
	#browser.get(campaign_url)
	#soup = BeautifulSoup(browser.page_source,'html.parser')
	#browser.quit()
		
	return Campaign(campaign_url=campaign_url)


def start_browser(browser=None,driver_binary=None):
	if browser=='Safari':
		browser = webdriver.Safari(executable_path=driver_binary);
	if browser=='Firefox':
		browser = webdriver.Firefox(executable_path=driver_binary);
	if browser=='Chrome':
		browser = webdriver.Chrome(executable_path=driver_binary);
	
	return browser

