import sys
sys.path.append(r'C:\\Users\\W-book\\.virtualenvs\\automation_job-hsQ2VWpp\\lib\\site-packages')
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime, timedelta
import re

from time import time,strftime
from time import sleep
import pandas as pd
from random import randint

from tqdm import tqdm

import os
os.chdir = os.path.abspath(os.getcwd())



def main():
	PATH = "./static/chromedriver"
	driver = webdriver.Chrome(PATH)

	base_url="https://www.parisjob.com/emplois/"
	query = "recherche.html?k="
	job = "data+scientist"
	zone = "&l=france&l_autocomplete=france&ray=10&"
	contract = "c=CDI&c=CDD&c=Stage&c=Independant&c=Alternance&"
	param = "d=w&p="
	num_page = '1'
	url = base_url + query + job + zone + contract + param + num_page

	# driver = webdriver.Chrome(PATH)
	# url = 'https://www.parisjob.com/emplois/alternant-data-science-h-f-7216168.html'
	# driver.get(url)
	# driver.find_element_by_xpath('/html/body/header/section[1]').find_elements_by_tag_name('a')[0].get_attribute('href')
	import sqlite3
	conn = sqlite3.connect('./data/NW_DB.db')
	c = conn.cursor()


	def add_data(company ,job_title ,describtion ,jobdate,text,joblink ,date,im,postuler,job_type ):
		c.execute('INSERT INTO jobtable(company,job_title,Describtion,jobdate,text,joblink,date,im,postuler,job_type) VALUES (?,?,?,?,?,?,?,?,?,?)',
	           (company ,job_title ,describtion ,jobdate,text ,joblink,date ,im,postuler,job_type ))
		conn.commit()

	def check_if_link_exist(value):
	    c.execute("SELECT * FROM jobtable WHERE joblink = ?", (value,))
	    data=c.fetchall()
	    if len(data)==0:
	        return False
	    else:
	        return True

	def text_before(value, a):
	    for val in a:
	        try:
	            message = value.split(val)[0]
	        except:
	            message = value

	    return message

	def fill_my_database(jobs_link, job_type):
	    print("Loading data in database ( {} new lines )...".format(len(jobs_link)))
	    try:
	        for Job in tqdm(jobs_link):
	            jobdate = jobs_link[Job]
	            date = get_date_of_publication(jobs_link[Job])
	            driver.get(Job)
	            try:
	                im = driver.find_element_by_xpath('/html/body/header/section[1]/img[2]').get_attribute('src')
	            except:
	                try:
	                    im = driver.find_element_by_xpath('/html/body/main/section[1]').find_elements_by_tag_name('img')[0].get_attribute('src')
	                except:
	                    im = ''

	            Head = driver.find_element_by_xpath('/html/body/header/section[1]/h1').text
	            company = Head.splitlines()[0]
	            job_title = Head.splitlines()[1]
	            job_describtion = driver.find_element_by_xpath('/html/body/header/section[1]/ul').text.splitlines()
	            #contract ,location ,work ,degree ,experience = get_attribute_of_a_job(job_describtion)
	            text = text_before(driver.find_element_by_xpath('/html/body/main/section[1]').text,["\nEn résumé ...\n","\nCalculez votre temps\n"])
	            try:
	                postuler = driver.find_element_by_xpath('/html/body/header/section[1]').find_elements_by_tag_name('a')[0].get_attribute('href')
	            except:
	                postuler = Job
	            add_data(company ,job_title ,str(job_describtion) ,jobdate,text,Job,date,im,postuler, job_type )
	        print("done!")
	    except:
	        print("not able to add data !")

	def get_date_of_publication(text=''):

	    if 'heures' in text or 'heure' in text:
	        date = datetime.now().date()
	    elif 'minutes' in text or 'minute' in text:
	        date = datetime.now().date()
	    elif 'jours' in text or 'jour' in text:
	        v = int(text.split(' a ')[1].split(' ')[0])
	        d = datetime.today() - timedelta(days=v)
	        date = d.date()
	    elif text=='hier':
	        d = datetime.today() - timedelta(days=1)
	        date = d.date()
	    elif text=='avant-hier':
	        d = datetime.today() - timedelta(days=2)
	        date = d.date()
	    elif text == 'le mois dernier':
	        d = datetime.today() - timedelta(days=30)
	        date = d.date()
	    else:
	        d = datetime.strptime(text, '%d/%m/%Y')
	        date = d.date()
	    return date

	def find_number_of_page(driver=None):

	    try:
	        jobs_size = WebDriverWait(driver, 20).until(
	             EC.presence_of_element_located((By.XPATH, r'/html/body/main/section[1]/div/section[2]/div[3]'))
	        )
	        jobs_size = jobs_size.text
	            # Calculating number of pages to be crawled (number of jobs available - number of jobs per page (here, 30))
	        job_number = int([i for i in jobs_size.split('\n')[0].split(' ') if i.isdigit()][1])
	        exact_page_nb = job_number / 20
	        #print("- Exact number of pages to be crawled : {}" .format(exact_page_nb))
	        min_page_nb = job_number // 20
	        #print("- Minimum number of pages to be crawled : {}" .format(min_page_nb))

	        if exact_page_nb > min_page_nb:
	            page_nb = min_page_nb + 2
	        elif exact_page_nb == min_page_nb:
	            page_nb = min_page_nb + 1
	    except  :

	         print("type error : Can't get job size from url" )
	         page_nb = 3
	        # First, get the number of jobs available

	    return page_nb

	def get_jobs_links_from_a_page(url=url):

	    driver.get(url)

	    try:
	        main = WebDriverWait(driver, 20).until(
	             EC.presence_of_element_located((By.XPATH, '/html/body/main/section[1]/div/section[2]/ul[1]'))
	        )
	    except Exception as e :
	        print("type error: " + str(e))
	        driver.quit()

	    list_links=main.find_elements_by_tag_name('a')
	    list_description = main.find_elements_by_class_name('time')
	    jobs={}
	    jobs_link = []
	    jobs_description = []
	    status = 'success'
	    try:
	        for i in list_links :
	            if (i.get_attribute('href') not in jobs_link):
	                jobs_link.append(i.get_attribute('href') )

	        for j in list_description:
	            jobs_description.append(j.text)

	        jobs = dict(zip(jobs_link, jobs_description))
	    except:
	        status = 'failed'

	    return {'jobs' : jobs, "status" : status}

	def check_if_job_exist_in_data(link, date):
	    c.execute("SELECT * FROM jobtable WHERE (joblink = '{}' AND date = '{}')".format(link,date))
	    data=c.fetchall()
	    if len(data)==0:
	        return False
	    else:
	        return True

	def find_new_jobs_in_website(job='', pages=[]):
		new_jobs = {}
		print(pages)
		for page_num in pages:
			print(page_num)
			url = base_url + query + job + zone + contract + param + page_num
			st = 'failed'
			essai = 0
			while (st == 'failed' and essai < 3):
				jobs_links_from_a_page = get_jobs_links_from_a_page(url=url)
				jobs = jobs_links_from_a_page['jobs']
				st = jobs_links_from_a_page['status']
				essai+=1
			if len(jobs)==0:
				pass
			else:
				for l in jobs:
					test = check_if_job_exist_in_data(l,get_date_of_publication(jobs[l]))
					if test==False:
						new_jobs.update({l : jobs[l]})
					else:
						pass
		return new_jobs

	job_list = ["data+scientist","data+analyst"]
	for job in tqdm(job_list):
		print('##################### {} ####################'.format(job))
		url = base_url + query + job + zone + contract + param + '1'
		driver.get(url)
		page_nb = find_number_of_page(driver)
		pages = [str(i) for i in range(1, page_nb)]
		new_jobs = find_new_jobs_in_website(job, pages)
		fill_my_database(new_jobs,job.replace('+',' '))



#
#max(pd.read_sql_query("SELECT * FROM jobtable", conn).date.unique())

if __name__=='__main__':
	main()
