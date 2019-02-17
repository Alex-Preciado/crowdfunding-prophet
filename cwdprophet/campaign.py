# cwdprophet
# Created by Jorge Alejandro Preciado Lopez on 2019-02-17.

class Campaign:
	'''
	Attributes:
	'''

	def __init__(self,campaign_url=None):
		self.campaign_url = campaign_url
	
	def copy(self):

		"""
		Return a copy of the Campaign object.
		Args:
			
		Returns:
			(Campaign): copy of the Image.
		"""
		# Make new  image with primary polarization
		newcampaign = Campaign(self.campaign_url)
		return newcampaign

		
def load_campaign(campaign_url,display=False):

	"""
	Read in an image from a text file.
	Args:
		url (str): URL of campaign
	Returns:
		(Campaign): loaded Campaign object
	"""


	print('Loaded campaign from:',campaign_url)
	
	return Campaign(campaign_url=campaign_url)