# auth_search.py: Search for available places in requested courses (via the Minerva interface)
# This file is from Minervac, a command-line client for Minerva
# <http://npaun.ca/projects/minervac>
# (C) Copyright 2016-2017 Nicholas Paun

import urllib,sys,auth_search_parse
from minerva_common import *

def make_course_request(term,subjects):
	request = [
			('rsts','dummy'),
			('crn','dummy'), 	# This is the CRN
			('term_in', term), 		# Term of search
			('sel_day','dummy'),
			('sel_schd','dummy'),
			('sel_insm','dummy'),
			('sel_camp','dummy'),
			('sel_levl','dummy'),
			('sel_sess','dummy'),
			('sel_instr','dummy'),
			('sel_ptrm','dummy'),
			('sel_attr','dummy'),
			('sel_subj','dummy')]

	for subj in subjects: request.append(('sel_subj',subj))
	request.extend([
			('sel_crse',''),	# Course code
			('sel_title',''),
			('sel_schd','%'),
			('sel_from_cred',''),
			('sel_to_cred',''),
			('sel_levl','%'),
			('sel_ptrm','%'),
			('sel_instr','%'),
			('sel_attr','%'),
			('begin_hh','0'),
			('begin_mi','0'),
			('begin_ap','a'),
			('end_hh','0'),
			('end_mi','0'),
			('end_ap','a'),
			('SUB_BTN','Get Course Sections'),
			('path','1')
		])	#This is seriously what Minerva shoves into a search form

	return urllib.urlencode(request)

def make_course_request_single(term, subject, number):
	request = [
		('term_in', term),
		('sel_subj', "dummy"), #WHY
		('sel_subj', subject),
		('SEL_CRSE', number),
		('SEL_TITLE', ''),
		('BEGIN_HH', '0'),
		('BEGIN_MI', '0'),
		('BEGIN_AP', 'a'),
		('SEL_DAY', 'dummy'),
		('SEL_PTRM', 'dummy'),
		('END_HH', '0'),
		('END_MI', '0'),
		('END_AP', 'a'),
		('SEL_CAMP', 'dummy'),
		('SEL_SCHD', 'dummy'),
		('sel_schd','%'),
		('SEL_SESS', 'dummy'),
		('SEL_INSTR', 'dummy'),
		('SEL_ATTR', 'dummy'),
		('SEL_LEVL', 'dummy'),
		('sel_levl','%'),
		('sel_ptrm','%'),
		('sel_instr','%'),
		('sel_attr','%'),
		('SEL_INSM', 'dummy'),
		('sel_dunt_code', ''),
		('sel_dunt_unit', ''),
		('call_value_in', ''),
		('rsts', 'dummy'),
		('crn', 'dummy'),
		('path', '1'),
		('SUB_BTN', 'View Sections')]
	return urllib.urlencode(request)

def dummy_course_request(term):
	return "rsts=dummy&crn=dummy&term_in=" + term + "&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_crse=&sel_title=&sel_from_cred=&sel_to_cred=&sel_ptrm=%25&begin_hh=0&begin_mi=0&end_hh=0&end_mi=0&begin_ap=x&end_ap=y&path=1&SUB_BTN=Advanced+Search" # Copied and pasted

def dummy_courselist_request(term, subject):
	return "rsts=dummy&crn=dummy&term_in=" + term + "&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=" + subject + "&sel_crse=&sel_title=&sel_from_cred=&sel_to_cred=&sel_ptrm=%25&begin_hh=0&begin_mi=0&end_hh=0&end_mi=0&begin_ap=x&end_ap=y&path=1&SUB_BTN=Course+Search"

def search_single(term, code):
	(subject, number, _) = code.split("-")
	r = minerva_post("bwskfcls.P_GetCrse", make_course_request_single(term, subject, number))
	return auth_search_parse.search_parse(r.text)

def search(term,course_codes):
	minerva_get("bwskfcls.p_sel_crse_search")
	minerva_post("bwskfcls.bwckgens.p_proc_term_date",{'p_calling_proc': 'P_CrseSearch','search_mode_in': 'NON_NT', 'p_term': term})
	if len(course_codes) == 1:
		return search_single(term, course_codes[0])

	subjects = []
	for code in course_codes:
		subjects.append(code.split("-")[0])

	
	minerva_post("bwskfcls.P_GetCrse",dummy_course_request(term))
	r = minerva_post("bwskfcls.P_GetCrse_Advanced",make_course_request(term,subjects))
	return auth_search_parse.search_parse(r.text)
