import sys
sys.path.append(r'C:\\Users\\W-book\\.virtualenvs\\automation_job-hsQ2VWpp\\lib\\site-packages')
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

from time import time,strftime
import pandas as pd

from tqdm import tqdm

import os
os.chdir = os.path.abspath(os.getcwd())

# c.execute("DELETE FROM jobtable WHERE job_type = '{}'".format("data analyst"))
# conn.commit()
# #
#pd.read_sql_query("SELECT * FROM jobtable", conn)

def main():
	PATH = "./static/chromedriver"
	driver = webdriver.Chrome(PATH)

	base_url =  "https://www.welcometothejungle.com/fr/jobs"
	query = "?query="
	job_list = ["data scientist","data analyst"]
	page = "&page="
	num_page = "1"
	zone ="&aroundQuery=France%2C%20France&"
	country_code = "refinementList%5Boffice.country_code%5D%5B%5D=FR&"
	CDI = "refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&"
	stage = "refinementList%5Bcontract_type_names.fr%5D%5B%5D=Stage&"
	freelance = "refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance&"
	CDD = "refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&"
	sort = "sortBy=mostRecent"

	# DB
	import sqlite3
	conn = sqlite3.connect('./data/DB.db')
	c = conn.cursor()

	def add_data(company ,job_title ,describtion ,jobdate,text,joblink ,date,im,job_type ):
		c.execute('INSERT INTO jobtable(company,job_title,Describtion,jobdate,text,joblink,date,im,job_type) VALUES (?,?,?,?,?,?,?,?,?)',
	           (company ,job_title ,describtion ,jobdate,text ,joblink,date ,im,job_type ))
		conn.commit()

	def check_if_job_exist_in_data(link, date,type):
	    c.execute("SELECT * FROM jobtable WHERE (joblink = '{}' AND date = '{}' AND job_type = '{}')".format(link,date,type))
	    data=c.fetchall()
	    if len(data)==0:
	        return False
	    else:
	        return True

	def find_number_of_page(driver=None):

	    try:
	        jobs_size = WebDriverWait(driver, 10).until(
	             EC.presence_of_element_located((By.XPATH, r'//*[@id="prc-1-1"]/div/main/section/div/header/div'))
	        )
	        jobs_size = jobs_size.text
	            # Calculating number of pages to be crawled (number of jobs available - number of jobs per page (here, 30))
	        job_number = jobs_size.split(" ",1)
	        job_number = int(job_number[0])
	        #print("- Number of open positions : {}" .format(job_number))
	        exact_page_nb = job_number / 30
	        #print("- Exact number of pages to be crawled : {}" .format(exact_page_nb))
	        min_page_nb = job_number // 30
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

	def get_jobs_links_from_a_page(url=None):

	    driver.get(url)

	    try:
	        main = WebDriverWait(driver, 20).until(
	             EC.presence_of_element_located((By.XPATH, '//*[@id="prc-1-1"]/div/main/section/div/ol'))
	        )
	    except Exception as e :
	        print("type error: " + str(e))
	        driver.quit()

	    list_links=main.find_elements_by_tag_name('a')
	    list_description = main.find_elements_by_tag_name('ul')
	    jobs={}
	    jobs_link = []
	    jobs_description = []
	    status = 'success'
	    try:
	        for i in list_links :
	            if (i.get_attribute('href') not in jobs_link):
	                jobs_link.append(i.get_attribute('href') )

	        for j in list_description:
	            jobs_description.append(j.text.splitlines()[2])

	        jobs = dict(zip(jobs_link, jobs_description))
	    except:
	        status = 'failed'

	    return {'jobs' : jobs, "status" : status}

	def get_date_of_publication(text=''):

	    if 'heures' in text or 'minutes' in text:
	        date = datetime.now().date()
	    elif 'jours' in text:
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
	        d = datetime.today() - timedelta(days=60)
	        date = d.date()
	    return date

	def fill_my_database(jobs_link, job_type):
	    try:
	        print("Loading data in database ( {} new lines )...".format(len(jobs_link)))
	        for Job in tqdm(jobs_link):
	            jobdate = jobs_link[Job]
	            date = get_date_of_publication(jobs_link[Job])

	            driver.get(Job)
	            im = driver.find_element_by_xpath('//*[@id="prc-1-1"]/main/section[1]/div/a/div/img').get_attribute('src')
	            company = driver.find_element_by_xpath('//*[@id="prc-1-1"]/main/section[1]/div/a/h3').text
	            job_title = driver.find_element_by_xpath('//*[@id="prc-1-1"]/main/section[1]/div/h1').text
	            job_describtion = driver.find_element_by_xpath('//*[@id="prc-1-1"]/main/section[1]/div/ul').text.splitlines()
	            #contract ,location ,work ,degree ,experience = get_attribute_of_a_job(job_describtion)
	            text = driver.find_element_by_xpath('//*[@id="prc-1-1"]/main/section[2]/div/div[2]').text
	            add_data(company ,job_title ,str(job_describtion) ,jobdate,text,Job,date,im, job_type )
	        print("done!")
	    except:
	        print("no job to add ! ")

	def find_new_jobs_in_website(job, pages):
		print(pages)
		exist=bool()
		i = 0
		new_jobs = {}
		while(exist==False and i < (len(pages))):
			print(i)
			page_num = pages[i]
			recherche = [query,job,page,page_num,zone,country_code,CDI,stage,freelance,CDD,sort]
			url = base_url + "".join(recherche[i] for i in range(len(recherche)) )
			st = 'failed'
			essai = 0
			while (st == 'failed' and essai < 3):
				jobs_links_from_a_page = get_jobs_links_from_a_page(url=url)
				jobs = jobs_links_from_a_page['jobs']
				st = jobs_links_from_a_page['status']
				essai+=1
			if len(jobs)==0:
				exist=False
			else:
				for l in jobs:
					test = check_if_job_exist_in_data(l,get_date_of_publication(jobs[l]),job)
					if test==False:
						new_jobs.update({l : jobs[l]})
					else:
						exist=True
						break
			i+=1
		return new_jobs

	for job in job_list:
		print('##################### {} ####################'.format(job))
		url = base_url + query+job+page+num_page+zone+country_code+CDI+stage+freelance+CDD+sort
		driver.get(url)
		page_nb = find_number_of_page(driver)
		pages = [str(i) for i in range(1, page_nb)]
		new_jobs = find_new_jobs_in_website(job,pages)
		fill_my_database(new_jobs,job)



if __name__=='__main__':
	main()
