#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import lxml.html
import pandas as pd


def get_html(url):         
	r = requests.get(url)  #response
	return r.text          #возвращает HTML код страницы (url)

def get_product_links(html):
	soup = BeautifulSoup(html, 'lxml')
	href = soup.find("ul", class_="products row clearfix products-narrow calc-height use-icon noprice-on-image")
	div = href.find_all('a', class_='product-loop-title')
	#список объектов супа
	links_of_products = []
	for td in div:
		a = td.get('href') # string
		links_of_products.append(a)
		#print(a)
	return links_of_products  			#список ссылок с главной


def get_page_2(html):
	soup = BeautifulSoup(html, 'lxml')
	paggination = soup.find('ul', class_='page-numbers')
	pag = paggination.find('a').get('href')
	return pag #возвращает вторую страницу, если товаров больше 50 они на второй странице, больше 100 я не встречал лол


def parse(html):
		html_tree = lxml.html.fromstring(html)
		soup = BeautifulSoup(html, 'lxml')
		pic = soup.find('a', class_='woocommerce-main-image').get('href')
		path = ".//div[@class='col-lg-6 col-md-5 col-sm-12 summary entry-summary']"
		#.//div[@class='col-lg-6 col-md-5 col-sm-12 summary entry-summary']
		last_offer = html_tree.xpath(path)[0]
		title = last_offer.xpath('./h1/text()')[0]
		price = last_offer.xpath("./p[@class='price']//text()")[0]
		descr = last_offer.xpath("./div[@class='description']/p//text()")[0:-1]
		
		data = {
			'title': title,
			'price': price,
			'descr': descr,
			'pic': pic,
		}

		return data

def write_csv(data):
	with open('data.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow((data['title'],
						 data['price'],
						data['descr'],
						data['pic']))

		print(data['title'], 'Спаршено') 	#записывает данные в CSV

#Основная функция - которая вызывает все остальные
def main():			
	#'https://xn--80apajghkndpd.xn--p1ai/shop/standartnyie-izdeliya/%D0%BF%D0%B0%D0%BB%D1%8C%D1%86%D1%8B/%D0%BF%D0%B0%D0%BB%D0%B5%D1%86-%D0%BD%D0%B0%D0%B2%D0%B5%D1%81%D0%BA%D0%B8-14%D1%8580/')
	
	#print(get_main_links(get_html('https://xn--80apajghkndpd.xn--p1ai/shop/')))
	#print(get_product_links(get_html('https://xn--80apajghkndpd.xn--p1ai/product-category/standartnyie-izdeliya/%d0%bf%d0%be%d0%b4%d1%88%d0%b8%d0%bf%d0%bd%d0%b8%d0%ba%d0%b8/'))) #подраздел подшипники
	#parse(get_html('https://xn--80apajghkndpd.xn--p1ai/shop/standartnyie-izdeliya/%D0%BF%D0%B0%D0%BB%D1%8C%D1%86%D1%8B/%D0%BF%D0%B0%D0%BB%D0%B5%D1%86-%D0%BD%D0%B0%D0%B2%D0%B5%D1%81%D0%BA%D0%B8-14%D1%8580/'))

	Base_of_url = 'http://xn--80apajghkndpd.xn--p1ai/product-category/standartnyie-izdeliya/%d0%bf%d0%be%d0%b4%d1%88%d0%b8%d0%bf%d0%bd%d0%b8%d0%ba%d0%b8/'#подшипники
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/standartnyie-izdeliya/%d0%bf%d0%b0%d0%bb%d1%8c%d1%86%d1%8b/'#пальцы
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/standartnyie-izdeliya/%d1%81%d0%b0%d0%bb%d1%8c%d0%bd%d0%b8%d0%ba%d0%b8/',
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/standartnyie-izdeliya/prochee-standartnoe/',
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/standartnyie-izdeliya/%d0%ba%d0%be%d0%bb%d1%8c%d1%86%d0%b0/',
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/reklamnaya-produktsiya/',
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/kardannyie-valyi/',
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/%d1%84%d0%b8%d0%bb%d1%8c%d1%82%d1%80%d0%b0/',
					#'https://xn--80apajghkndpd.xn--p1ai/product-category/%d0%b7%d0%b8%d0%bf/']
	#ssilki = []
	#for q in Base_of_url:
	all_links_main = get_product_links(get_html(Base_of_url))
	try:
		find_link_page_2 = get_page_2(get_html(Base_of_url))
		links_page_2 = get_product_links(get_html(Base_of_url))
		all_links_main = all_links_main + links_page_2
	except: pass
		#ssilki.append(all_links_main)

	

	
	#products = parse(get_html('https://xn--80apajghkndpd.xn--p1ai/shop/standartnyie-izdeliya/%d0%bf%d0%be%d0%b4%d1%88%d0%b8%d0%bf%d0%bd%d0%b8%d0%ba%d0%b8/%d0%bf%d0%be%d0%b4%d1%88%d0%b8%d0%bf%d0%bd%d0%b8%d0%ba-%d0%b8%d0%b3%d0%be%d0%bb%d1%8c%d1%87%d0%b0%d1%82%d1%8b%d0%b9-25%d1%85198-d06-309-2-5x19-8/'
#))
#add-links-wrap	

	for i in all_links_main:
		product = parse(get_html(i))
		print(product)
		write_csv(product)
	


if __name__ == '__main__':
	main()
