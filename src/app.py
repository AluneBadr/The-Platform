

import os
os.chdir = os.path.abspath(os.getcwd())

import streamlit as st
from PIL import Image
icone = Image.open('./static/icone2.PNG')
st.set_page_config(page_title='Hello Word', page_icon=icone,layout="wide")
import webbrowser
import pandas as pd

from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

from time import time,strftime


from tqdm import tqdm


import sqlite3
conn = sqlite3.connect('./data/DB.db')
c = conn.cursor()
#MAJ

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



#	st.warning("Update failed !")


# Layout Templates
title_temp ="""
	<div style="background-color:#2874A6 ;padding:1px;border-radius:5px;margin:2px;">
    <a href="{}" target="_blank" </a>
    <h6 style="color:white;text-align:center;">{}</h6>
    <h4 style="color:white;text-align:center;">{}</h1>
	<img src={} alt="Avatar" style="vertical-align: middle;float:left;width: 60px;height: 60px;border-radius: 50%;" >
	<h6 style="color:white;text-align:center;">{}</h6>
	<br/>
	<br/>
	<p style="text-align:center">Publication date : {}</p>
	</div>
	"""
article_temp ="""
	<div  style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
    <h6 style="color:white;text-align:center;">{}</h6>
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6>
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:center">{}</p>
	</div>
	"""
head_message_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
	<h6>Author:{}</h6>
	<h6>Post Date: {}</h6>
	</div>
	"""

button_temp ="""
	<form action="{}" target="_blank"> <input type="submit" value=" Apply " /> </form>

	"""


full_message_temp ="""
	<p style="text-align:justify;color:black;white-space:pre-line;padding:10px">{}</p>

	"""

def replace():
	c.execute("UPDATE jobtable SET  job_title = REPLACE(job_title, 'Datascientist', 'Data scientist ')")
	conn.commit()

def view_jobs_3_arg(col1,val1,col2,val2,col3,val3):
	data = pd.read_sql_query('SELECT * FROM jobtable WHERE ({} LIKE "%{}%" AND {} LIKE "%{}%" AND {} LIKE "%{}%")'.format(col1,val1,col2,val2,col3,val3), conn)
	#data = c.fetchall()
	return data

def view_jobs_2_arg(col1,val1,col2,val2):
	data = pd.read_sql_query('SELECT * FROM jobtable WHERE ({} LIKE "%{}%" AND {} LIKE "%{}%")'.format(col1,val1,col2,val2), conn)
	#data = c.fetchall()
	return data

def view_jobs_1_arg(col1,val1):
	data = pd.read_sql_query('SELECT * FROM jobtable WHERE {} LIKE "%{}%"'.format(col1,val1), conn)
	#data = c.fetchall()
	return data

def Display(data):
	j=0
	for i, row in data.iterrows():
		j+=1
		b_company = row['company']
		b_title = row['job_title']
		b_desc = "  -*-   ".join( i for i in eval(row['Describtion']))
		b_im = row['im']
		b_post_date = row['date']
		b_text = row['text']
		b_link = row['joblink']
		b_post = row['postuler']
		st.markdown(title_temp.format(b_link,b_company,b_title,b_im,b_desc,b_post_date),unsafe_allow_html=True)
		col1,col2 = st.beta_columns([12,1])
		with col1:
			if st.button("Describtion", key=j):
				st.markdown(full_message_temp.format(b_text),unsafe_allow_html=True)
				if st.checkbox('hide',key=j):
					st.markdown(full_message_temp.format(' '),unsafe_allow_html=True)
		with col2:
			st.markdown(button_temp.format(b_post),unsafe_allow_html=True)
            #if st.button("Apply", key=j):
                #webbrowser.open_new_tab(b_post)

def main():

	html_temp="""
    	<div style="width:500px; margin:0 auto;background-color:{};padding:5px;border-radius:10px">
        <p style = "font-family:AmstelvarAlpha,arial,helvetica;font-size: 4rem;line-height: 4.8rem;"> THE PLATFORM </p>
    	</div>
	"""
	st.markdown(html_temp.format('white'),unsafe_allow_html=True)

	st.write('\n')
	st.write('\n')
	st.write('\n')
	jobs = ["Data Scientist","Data Analyst", "Data Engineer"," "]
	jb = st.sidebar.selectbox("What job do you search ?",jobs)

	contract = ["CDI","CDD","Stage", "Freelance" ]
	ctra = st.sidebar.selectbox("Contract",contract)

	lieu = st.sidebar.text_input('Where ?', "Paris")

	if lieu in ["France", "france", "FRANCE"]:
		if jb == " ":
			result = view_jobs_1_arg("Describtion", ctra)
		else:
			replace()
			result = view_jobs_2_arg("job_title", jb , "Describtion" , ctra)
	else:
		if jb == " ":
			result = view_jobs_2_arg("Describtion", lieu, "Describtion", ctra)
		else:
			replace()
			result = view_jobs_3_arg("job_title", jb ,"Describtion", lieu, "Describtion", ctra)

	st.sidebar.subheader('Search by Company name : ')
	cpny=st.sidebar.text_input('Company name', "")
	if cpny :
		result = pd.read_sql_query('SELECT * FROM jobtable WHERE {} = "{}"'.format("company", cpny.upper()), conn)

	if st.sidebar.checkbox('sort by date'):
		result = result.sort_values(['date'], ascending=False)


	if len(result) >= 30:
		exact_page_nb = len(result) / 30
        #print("- Exact number of pages to be crawled : {}" .format(exact_page_nb))
		min_page_nb = len(result) // 30
        #print("- Minimum number of pages to be crawled : {}" .format(min_page_nb))
		if exact_page_nb > min_page_nb:
			page_nb = min_page_nb + 1
		elif exact_page_nb == min_page_nb:
			page_nb = min_page_nb

		Pages = [i for i in range(page_nb)]
		pg = st.sidebar.selectbox('Page', Pages)
		From = pg*30
		To=pg*30+29
		df = result.iloc[From:To,]
		Display(df)
	else:
		Display(result)

	if st.sidebar.button("Refresh !", key=200):
		exec(open("./src/update.py").read())

	l_upd = max(pd.read_sql_query("SELECT * FROM jobtable", conn).date.unique())
	st.sidebar.success("Last Update : {}".format(l_upd))

	# st.sidebar.subheader('Get new Publications : ')
	# Websites = ["Welc. to the jug.","Paris Job" ]
	# ws = st.sidebar.selectbox("From",Websites)
	# if st.sidebar.button("Go !", key=200):
	# 	if ws=="Paris Job":
	# 		exec(open("./src/maj_pj.py").read())
	# 	else:
	# 		exec(open("./src/maj_wtjj.py").read())



if __name__ == '__main__':
    main()
