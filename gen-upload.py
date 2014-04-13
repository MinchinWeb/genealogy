#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Genealogy Uploader
v.3.0 - WM - April 12, 2014

This script serves to semi-automate the building and uploading of my
genealogy website. It is intended to be semi-interactive and run from the
command line.'''

__version__ = 3.0


from datetime import datetime
from datetime import date
import colorama
from colorama import Fore, Back, Style
colorama.init()
import re
import fileinput
import textwrap
import webbrowser
import os
import zipfile
import uuid
import sys
import winshell
import requests
from bs4 import BeautifulSoup
# import envoy
import wmtext
from fabric.api import local, task, env


env.github_folder = "S:\\Documents\\GitHub\\genealogy-gh-pages"
env.photo_folder = "S:\\Documents\\genealogy"
env.download_folder = "S:\\Downloads\\Firefox"
env.url_root = "http://minchin.ca/genealogy"
env.repo_url = "https://github.com/MinchinWeb/genealogy.git"
env.adam_prefix = 'adam-1246-'
env.today = '' + str(date.today().year)[2:] + str.zfill(str(date.today().month), 2) + str.zfill(str(date.today().day), 2)
env.gedcom_expected = 'William ' + env.today + '.ged'
env.my_gedcom = winshell.desktop() + "\\" + env.gedcom_expected
#start_time = datetime.now()
env.step_no = 0 # step counter
env.start_time = datetime.now()
env.working_folder = os.getcwd()	# current working directory
env.content_folder = env.working_folder + '\\content\\pages'
env.adam_zip = 'adam.zip'		# set later


def addimage(image):
	'''Take the file listed in image, finds in my genealogy photo directory, and
	adds it to the GitHub folder.'''
	'''TO-DO: implement this!!'''
	pass


# multiple replacement
# from 	http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
#
# Usage:
# >>> replacements = (u"café", u"tea"), (u"tea", u"café"), (u"like", u"love")
# >>> print multiple_replace(u"Do you like café? No, I prefer tea.", *replacements)
# Do you love tea? No, I prefer café.
def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M | re.I)
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)


def get_adam_version():
	soup_file = open(env.content_folder + '\\names.html', 'r')
	soup = BeautifulSoup(soup_file)
	soup_file.close()
	return soup.find(True, "adam-version").get_text().encode('utf-8')[:-2] # 'Built by Adam 1.35.0.0' or the like


@task
def export_gedcom():
	'''Export from RootsMagic'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Export from RootsMagic.")

	print("        call the file " + Style.BRIGHT + env.gedcom_expected + Style.RESET_ALL + " and save it to the desktop")
	print("        do not include LDS information")
	print("        no need to privatize individuals (at this step)")
	if not wmtext.query_yes_quit("    Next?", default="yes"):
		sys.exit()
	try:
		env.start_time = datetime.fromtimestamp(os.stat(env.my_gedcom).st_ctime)
	except:
		print("    Your file doesn't seem to exist. Exiting...")


@task
def clean_gedcom():
	'''Cleaning up GEDCOM'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Cleaning up GEDCOM...")

	# replace image paths
	gedcom_file = file(env.my_gedcom, 'r') # add failsafe is the fail doesn't exist yet or is still being written to
	subject = gedcom_file.read()
	gedcom_file.close()

	pattern = re.compile(r'S:\\Documents\\Genealogy\\([0-9]+[\.[a-z]+]*\.? )*', re.IGNORECASE) # path start
	result = pattern.sub('images/', subject)
	pattern2 = re.compile(r'(images.*)\\') # reverse slashes in rest of path
	result2 = pattern2.sub(r'\1/', result)
	result3 = pattern2.sub(r'\1/', result2)

	f_out = file(env.my_gedcom, 'w')
	f_out.write(result3)
	f_out.close()


@task
def upload_gedcom():
	'''Upload GEDCOM to Adam'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". The file is now ready to upload to Adam.")

	webbrowser.open("http://timforsythe.com/tools/adam", new=2)
	print("        log-in (using Facebook)")
	print("        now click 'generate report'")
	# check to see if we're logged in
	# log in, if needed
	# discard old GEDCOM
	# upload new GEDCOM
	# run generator
	# download new output


@task
def check_images():
	'''Check which images have already been uploaded'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Checking images...")

	gedcom_file = open(env.my_gedcom, 'r')
	subject = gedcom_file.read()
	gedcom_file.close()

	missing_matches = []
	all_matches = []
	matches = 0
	wrapper = textwrap.TextWrapper(width=79, initial_indent=" "*6, subsequent_indent=" "*10)
	pattern_bad = re.compile("missing ")
	for match in re.findall(r'(images/.+\.(jpg|jpeg|png|gif|pdf))', subject, re.IGNORECASE):
		all_matches.append(match)
	
	all_matches = sorted(set(all_matches)) # remove duplicates and sort
	for match in all_matches:
		r = requests.head(env.url_root + "/" + str(match[0]), allow_redirects=True)
		if not r.status_code == requests.codes.ok:
			mytext = wrapper.fill("missing " + str(r.status_code) + " -> " + match[0])
			print pattern_bad.sub(Fore.RED + Style.BRIGHT + "missing " + Style.RESET_ALL, mytext)
			missing_matches.append(match[0])
		else:
			matches += 1

	if len(missing_matches) == 0:
		print("        " + str(matches) + " images matching. No missing images.")
	else:
		print("        " + str(matches) + " images matching.")
		q_add_images = wmtext.query_yes_no_all("        " + str(len(missing_matches)) + " missing images. Add them?", default="no")
		if q_add_images == 2: #all
			for image in missing_matches:
				addimage(image)
		elif q_add_images == 1: #yes
			for image in missing_matches:
				if wmtext.querry_yes_no("        Add " + image + "?", default="yes"):
					addimage(image)
					# TO-DO: implement this!
				else:
					pass
		else: #no
			pass
			
		# write missing images to a file
		f = open('missing-images.txt', 'w')
		f.write("Genealogy Uploader, v." + str(__version__) + '\n')
		f.write(env.my_gedcom + '\n')
		f.write('\n')
		for missing in missing_matches:
			f.write(missing + '\n')
		f.close()
		
@task
def delete_old_output():
	'''Delete old Pelican output'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Deleting old Pelican output.")

	to_delete = []
	html_files = 0
	os.chdir(env.github_folder)
	all_files = os.listdir(env.github_folder)

	for filename in all_files:
		if filename == ('.git'):
			pass
		elif filename.endswith('.html'):
			html_files += 1
		else:
			to_delete.append(filename)

	counter = 0
	
	# delete HTML files
	local('del *.html -y')
	bar = wmtext.progressbar(maximum = len(to_delete) + html_files)
	counter = html_files
	bar.update(counter)

	#delete everything else
	for myfile in to_delete:
		winshell.delete_file(myfile, no_confirm = True, allow_undo = False, silent = True)
		counter += 1
		bar.update(counter)
	print("\n      " + str(len(to_delete) + html_files) + " files deleted.")


@task
def delete_old_adam():
	'''Delete old Adam output'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Deleting old Adam output.")
	
	os.chdir(env.content_folder)
	local('del *.* /q')


@task	
def get_new_adam():
	'''Get new Adam output'''
	# TO-DO: allow override of 'start time'
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Get new Adam output.")

	os.chdir(env.download_folder)

	count_loops = 0
	while True:
		all_files = os.listdir(env.download_folder)
		for filename in all_files:
			if filename.startswith(adam_prefix) and filename.endswith(".zip"):
				if datetime.fromtimestamp(os.stat(filename).st_ctime) > local_start_time:
					env.adam_zip = filename
		if env.adam_zip != '' and os.stat(env.adam_zip).st_size > 1000:
			break
		count_loops +=1
		if count_loops > 60:
			if wmtext.query_yes_quit("    We've waited 30 minutes. Keep waiting?", default="yes") == False:
				sys.exit()
			else:
				count_loops = 0
		else:
			wmtext.wait(30)
		
	winshell.copy_file(env.adam_zip, env.content_folder)


def step_unzip():
	# 6:48.948 for 9,999 files
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(env.content_folder)
	zf = zipfile.ZipFile(env.adam_zip)
	zf.extractall()
	zf.close()


def step_unzip_faster():
	# see http://dmarkey.com/wordpress/2011/10/15/python-zipfile-speedup-tips/
	# 4:44.459 for 9,999 files
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(env.content_folder)
	zf = zipfile.ZipFile(open(env.adam_zip, 'r'))
	zf.extractall()
	zf.close()


def step_unzip_czip():
	# 4:46.109 for 9,999 files
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(env.content_folder)
	zf = czipfile.ZipFile(env.adam_zip)
	zf.extractall()
	zf.close()


def step_unzip_7zip():
	#  5:09.974 for 9,999 files
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Unzip new Adam output.")
	
	os.chdir(env.content_folder)
	local('"C:\\Program Files\\7-Zip\\7z.exe" e ' + env.adam_zip + ' > nul')
	print datetime.now() - env.start_time


@task
def unzip_adam():
	'''Unzip new Adam output'''
	step_unzip_faster()


@task
def replace_index():
	'''Copy over index.md, 404.md'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Copy over index.md, 404.md")

	os.chdir(env.content_folder)
	try:
		winshell.delete_file("index.md", no_confirm = True, allow_undo = False, silent = True)
	except:
		pass
	try:
		winshell.delete_file("404.md", no_confirm = True, allow_undo = False, silent = True)
	except:
		pass

	winshell.copy_file("../../_unchanging_pages/index.md", "index.md", no_confirm = True)
	winshell.copy_file("../../_unchanging_pages/404.md", "404.md", no_confirm = True)


@task
def set_pelican_variables():
	'''Sets a couple of variables that Pelican uses while generating the site.'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Setting up Pelican.")
	
	adam_version_text = get_adam_version() # 'Built by Adam 1.35.0.0 ' or the like
	date_in_text = date.today().strftime("%B %d, %Y").replace(' 0', ' ') # 'January 7, 2014' or the like
	f = open(env.working_folder + '\\adamconf.py', 'w')
	f.write("# Genealogy Uploader, v." + str(__version__) + '\n')
	f.write('# ' + env.my_gedcom + '\n\n')
	f.write('ADAM_VERSION = "' + adam_version_text + '"\n')
	f.write('ADAM_UPDATED = "' + date_in_text + '"\n')
	f.close()
	

@task	
def replace_emails():
	'''Hide emails in Sources'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Hiding Emails.")

	# replace and hide emails; but some of these are over lines breaks,
	#  so we'll have to search and replace through the output
	# We are actually only considering 'Sources', as that's where
	#  all the emails seem to be...
	replacements =	("w_minchin@hotmail.com",			'[email redacted]'), \
					("w.minchin@gmail.com",				'[email redacted]'), \
					("webmaster@minchin.ca",			'[email redacted]'), \
					("minchinweb@gmail.com",			'[email redacted]'), \
					("nysgys@shaw.ca",					'[email redacted]'), \
					("bunburypr@ozemail.com.au",		'[email redacted]'), \
					("turtle@turtlebunbury.com",		'[email redacted]'), \
					("howard.blaxland@gmail.com",		'[email redacted]'), \
					("kenhazel@gmail.com",				'[email redacted]'), \
					("canrcr@gmail.com",				'[email redacted]'), \
					("david@westerhamworkshop.co.uk",	'[email redacted]'), \
					("d3gl@shaw.ca",					'[email redacted]'), \
					("cardena.depper@gmx.net",			'[email redacted]'), \
					("redjoanne_58@hotmail.com",		'[email redacted]'), \
					("lbwong@charter.net",				'[email redacted]'), \
					("djcmgf@optonline.net",			'[email redacted]'), \
					("jerry.doyle@sbcglobal.net",		'[email redacted]'), \
					("sonofcam@bigpond.com",			'[email redacted]'), \
					("stewdee@hotmail.com",				'[email redacted]'), \
					("nysgys@shaw.ca",					'[email redacted]'), \
					("gloog@eircom.net",				'[email redacted]'), \
					("donaldminchin@yahoo.com",			'[email redacted]'),

	os.chdir(env.content_folder)
	all_files = os.listdir(env.content_folder)
	all_html_files = []
	for my_file in all_files:
		#if my_file.endswith(".html"):
		if my_file.startswith('sources-'):
			all_html_files.append(my_file)
	counter = 0
	bar = wmtext.progressbar(maximum = len(all_html_files))
	# inline search and replace
	for file in all_html_files:
		for line in fileinput.input(file, inplace=1):
			print multiple_replace(line, *replacements)
		counter += 1
		bar.update(counter)
	print # clear progress bar


@task
def clean_adam_html():
	'''Remove nasty and extra HTML.'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Remove nasty and extra HTML.")

	os.chdir(env.content_folder)
	all_files = os.listdir(env.content_folder)
	all_html_files = []
	for my_file in all_files:
		if my_file.endswith(".html"):
			all_html_files.append(my_file)

	counter = 0
	bar = wmtext.progressbar(maximum = len(all_html_files))
	for file in all_html_files:
		with open(env.content_folder + '\\' + file, 'r') as html_doc:
			my_html = html_doc.read()

		soup = BeautifulSoup(my_html)
		for tag in soup(property="og:title", limit=1):
			tag.decompose()
		for tag in soup(charset=True):
			tag.decompose()
		for tag in soup.find_all(id="site-header"):
			tag.decompose()
		for tag in soup(id="adam-page-title"):
			tag.decompose()
		for tag in soup(class_="adam-version", limit=1):
			tag.decompose()
		for tag in soup(id="site-footer"):
			tag.decompose()

		with open(env.content_folder + '\\' + file, 'w') as html_doc:
			html_doc.write(str(soup))

		counter += 1
		bar.update(counter)
	print # clear progress bar


@task
def pelican():
	'''Run Pelican'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Run Pelican (site generator)")
	
	os.chdir(env.working_folder)
	local ('pelican -s publishconf.py')


@task
def create_tracking():
	'''Create deploy tracking file'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Create deploy tracking file.")

	# create a 'random' number using UUID
	# note that the last set of digits will correspond to the workstation
	myUUID = str(uuid.uuid1())
	env.tracking_filename = myUUID + ".txt"
	target = open(env.github_folder + '\\' + env.tracking_filename, 'w')
	target.write(myUUID + "\n")
	target.write("Adam upload by Python script.\n")
	target.write(env.gedcom_expected + "\n")
	target.close()


@task
def git():
	'''Git commit and push'''
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Git -> commit and push")

	#commit_msg = "Adam generated upload from " + gedcom_expected
	os.chdir(env.github_folder)
	wmtext.clock_on_right(Fore.YELLOW + ' > git add -A' + Style.RESET_ALL)
	r1 = local('git add -A')
	print r1.std_err,
	wmtext.clock_on_right(Fore.YELLOW + '> git commit -m Adam_upload' + Style.RESET_ALL)
	r2 = local('git commit -m Adam_upload')
	print r2.std_out, r2.std_err,
	wmtext.clock_on_right(Fore.YELLOW + '> git push origin' + Style.RESET_ALL)
	r3 = local('git push origin')
	print r3.std_out, r3.std_err


@task
def live():
	'''Tell us when we're live'''
	# TO-DO: find tracking file based on creation/modified date
	env.step_no += 1
	wmtext.clock_on_right(str(env.step_no).rjust(2) + ". Wait to go live")
	
	if tracking_filename is None:
		print ('No tracking file set.')
	else:
		while True:
			r = requests.head(env.url_root + "/" + env.tracking_filename, allow_redirects=rue)
			if r.status_code == requests.codes.ok:
				break
			else:
				wmtext.wait(180)


@task
def all_steps():
	'''Everything!'''
	wmtext.title("Genealogy Uploader, v." + str(__version__))
	print
	
	export_gedcom()				# works
	clean_gedcom()				# works
	upload_gedcom()				# doesn't open webbrowser
	check_images()				# works
	delete_old_output()			# works
	delete_old_adam()			# works ~2 min
	get_new_adam()				#
	unzip_adam()				# pretty sure works ~5 min
	replace_index()				# works
	set_pelican_variables()		# works
	clean_adam_html()			# doesn't crash
	replace_emails()			# doesn't crash
	create_tracking()			# works ~10 sec
	pelican() 					# works (assuming Pelican works)
	git()						#
	live()						#
	
	wmtext.clock_on_right(Fore.GREEN + Style.BRIGHT + "Update is Live")
	print Style.RESET_ALL
	
	print datetime.now() - start_time

@task(default=True)
def does_nothing():
	print ('this does nothing')
	
				
if __name__ == "__main__":
	all_steps()
