

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
	<img src={} alt="" style="vertical-align: middle;float:left;width: 60px;height: 60px;border-radius: 50%;" >
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
deft = "data:image/png;base64,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"

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
		b_im = row['im'].replace('./static/defautl.png', deft)
		b_post_date = row['date']
		b_text = row['text']
		b_link = row['joblink']
		b_post = row['postuler']
		st.markdown(title_temp.format(b_link,b_company,b_title,b_im,b_desc,b_post_date),unsafe_allow_html=True)
		col1,col2 = st.columns([12,1])
		with col1:
			if st.button("Describtion", key=j):
				st.markdown(full_message_temp.format(b_text),unsafe_allow_html=True)
				if st.checkbox('hide',key=j+1000):
					st.markdown(full_message_temp.format(' '),unsafe_allow_html=True)
		with col2:
			st.markdown(button_temp.format(b_post),unsafe_allow_html=True)
            #if st.button("Apply", key=j):
                #webbrowser.open_new_tab(b_post)'


def main():

	html_temp="""
    	<div style="width:500px; margin:0 auto;background-color:{};padding:5px;border-radius:10px">
        <p style = "font-family:AmstelvarAlpha,arial,helvetica;font-size: 4rem;line-height: 4.8rem;"> THE PLATFORM </p>
    	</div>
	"""
	st.markdown(html_temp.format('white'),unsafe_allow_html=True)

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

	st.success('{} posts found ! '.format(len(result)))
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
		try:
			exec(open("./src/update.py").read())
		except:
			st.write("ERROR 503 :(")

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
