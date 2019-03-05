import time
import requests
import lxml.html
import json

class UralParser(object):
	"""docstring for UralParser"""
	def __init__(self, base_url):
		self.base_url = base_url
		self.last_time =''

	def get_page(self):

		try:
			res = requests.get(self.base_url)
		except requests.ConnectionError:
			return

		if res.status_code < 400:
			return res.content


	def parse(self, html):
		html_tree = lxml.html.fromstring(html)
		path = ".//div[@class='col-lg-6 col-md-5 col-sm-12 summary entry-summary']"
		#.//div[@class='col-lg-6 col-md-5 col-sm-12 summary entry-summary']
		last_offer = html_tree.xpath(path)[0]
		title = last_offer.xpath('./h1/text()')[0]
		price = last_offer.xpath("./p[@class='price']//text()")[0]
		descr = last_offer.xpath("./div[@class='description']/p//text()")[0:-1]


		
		result = {
			'title': title,
			'price': price,
			'descr': descr,
		}

		with open('data', 'w') as fp:

			json.dump(result, fp)
	

	'''def run(self):
		while True:
			page =  self.get_page()

			if page is None:
				time.sleep(0.5)
				continue

			self.get_last_offer(page)

			time.sleep(0.5)
	'''
if __name__ == "__main__":

	parser = UralParser('https://xn--80apajghkndpd.xn--p1ai/shop/standartnyie-izdeliya/%D0%BF%D0%B0%D0%BB%D1%8C%D1%86%D1%8B/%D0%BF%D0%B0%D0%BB%D0%B5%D1%86-%D0%BD%D0%B0%D0%B2%D0%B5%D1%81%D0%BA%D0%B8-14%D1%8580/')
	page = parser.get_page()

	parser.parse(page)

	#parser.run()
