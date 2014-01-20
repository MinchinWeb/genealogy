'''Genealogy Uploader
v.2 - WM - Jan. 6, 2014

This script serves to semi-automate the building and uploading of my
genealogy website. It is intended to be semi-interactive and run from the
command line.'''

__version__ = 2
github_folder = "S:\\Documents\\GitHub\\genealogy"
photo_folder = "S:\\Documents\\genealogy"
download_folder = "S:\\Downloads\\Firefox"
url_root = "http://minchin.ca/genealogy"
repo_url = "git@github.com:MinchinWeb/genealogy.git"
my_key_file = "C:\\Users\\William\\.ssh\\github_rsa"

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
import envoy
import wmtext

today = '' + str(date.today().year)[2:] + str.zfill(str(date.today().month), 2) + str.zfill(str(date.today().day), 2)
gedcom_expected = 'William ' + today + '.ged'
my_gedcom = winshell.desktop() + "\\" + gedcom_expected
#start_time = datetime.now()

def addimage(image):
	'''Take the file listed in image, finds in my genealogy photo directory, and
	adds it to the GitHub folder.'''
	'''TO-DO: implement this!!'''
	pass


wmtext.title("Genealogy Uploader, v." + str(__version__))
print
wmtext.clock_on_right(" 1. Export from RootsMagic.")
print("        call the file " + Style.BRIGHT + gedcom_expected + Style.RESET_ALL + " and save it to the desktop")
print("        do not include LDS information")
print("        no need to privatize individuals (at this step)")
if not wmtext.query_yes_quit("    Next?", default="yes"):
	sys.exit()

wmtext.clock_on_right(" 2. Cleaning up GEDCOM...")
start_time = datetime.fromtimestamp(os.stat(my_gedcom).st_ctime)
# replace image paths
gedcom_file = file(my_gedcom, 'r')
subject = gedcom_file.read()
gedcom_file.close()

pattern = re.compile(r'S:\\Documents\\Genealogy\\[0-9]+[\.[a-z]+]*\.? ') # path start
result = pattern.sub('images/', subject)
pattern2 = re.compile(r'(images.*)\\') # reverse slashes in rest of path
result2 = pattern2.sub(r'\1/', result)
result3 = pattern2.sub(r'\1/', result2)

f_out = file(my_gedcom, 'w')
f_out.write(result3)
f_out.close()

wmtext.clock_on_right(" 3. The file is now ready to upload to Adam.")
webbrowser.open("http://timforsythe.com/tools/adam", new=2)
print("        log-in (using Facebook)")
print("        now click 'generate report'")

wmtext.clock_on_right(" 4. Checking images...")
gedcom_file = open(my_gedcom, 'r')
subject = gedcom_file.read()
gedcom_file.close()

missing_matches = []
matches = 0
wrapper = textwrap.TextWrapper(width=79, initial_indent=" "*8, subsequent_indent=" "*12)
pattern_bad = re.compile("missing ")
for match in re.findall(r'(images/.+\.(jpg|jpeg|png|gif|pdf))', subject, re.IGNORECASE):
	r = requests.head(url_root + "/" + str(match[0]))
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
			else:
				pass
	else: #no
		pass

wmtext.clock_on_right(" 5. Deleting old Adam output.")
to_delete = []
os.chdir(github_folder)
all_files = os.listdir(github_folder)
for filename in all_files:
	if filename.startswith('adam_') and filename.endswith(".zip"):
		to_delete.append(filename)
	elif filename.endswith(".html"):
		to_delete.append(filename)
	elif filename.endswith(".png"):
		to_delete.append(filename)
	elif filename.endswith(".js"):
		to_delete.append(filename)
	elif filename in ["adam.css"]:
		to_delete.append(filename)
for myfile in to_delete:
	winshell.delete_file(myfile, no_confirm = True, allow_undo = False, silent = True)
	pass
print("        " + str(len(to_delete)) + " files deleted.")

wmtext.clock_on_right(" 6. Get new Adam output.")
adam_zip = ''
os.chdir(download_folder)

count_loops = 0
while True:
	all_files = os.listdir(download_folder)
	for filename in all_files:
		if filename.startswith('adam_') and filename.endswith(".zip"):
			if datetime.fromtimestamp(os.stat(filename).st_ctime) > start_time:
				adam_zip = filename
	if adam_zip != '' and os.stat(adam_zip).st_size > 1000:
		break
	count_loops +=1
	if count_loops > 60:
		if wmtext.query_yes_quit("    We've waited 30 minutes. Keep waiting?", default="yes") == False:
			sys.exit()
		else:
			count_loops = 0
	else:
		wmtext.wait(30)
	
winshell.copy_file(adam_zip, github_folder)

wmtext.clock_on_right(" 7. Unzip new Adam output.")
os.chdir(github_folder)
zf = zipfile.ZipFile(adam_zip)
zf.extractall()
zf.close()

wmtext.clock_on_right(" 8. Copy over index.html")
os.chdir(github_folder)
winshell.delete_file("index.html", no_confirm = True, allow_undo = False, silent = True)
winshell.copy_file("_adam/index.html", "index.html", no_confirm = True)

wmtext.clock_on_right(" 9. Replacing Adam version number.")
print("    Updated dates")
print("    Hiding emails")
soup_file = open('names.html', 'r')
soup = BeautifulSoup(soup_file)
soup_file.close()
adam_version_text = soup.find(True, "adam-version").get_text().encode('utf-8') # 'Built by Adam 1.35.0.0 ' or the like
date_in_text = date.today().strftime("%B %d, %Y").replace(' 0', ' ') # 'January 7, 2014' or the like
pattern = re.compile('(w_minchin@hotmail\.com|w\.minchin@gmail\.com|webmaster@minchin\.ca|nysgys@shaw\.ca|bunburypr@ozemail\.com\.au|turtle@turtlebunbury\.com|howard\.blaxland@gmail\.com|kenhazel@gmail\.com|canrcr@gmail\.com|david@westerhamworkshop\.co\.uk|d3gl@shaw\.ca|cardena\.depper@gmx\.net|redjoanne_58@hotmail\.com|lbwong@charter\.net)', re.I) # replace and hide emails; but some of these are over lines breaks, so we'll have to search and replace through the output

all_files = os.listdir(github_folder)
all_html_files = []
for my_file in all_files:
	if my_file.endswith(".html"):
		all_html_files.append(my_file)
# inline search and replace
for line1 in fileinput.input(all_html_files, inplace=1):
	line2 = line1.replace("$adam-version$", adam_version_text)
	line3 = line2.replace("$tree-updated$", date_in_text)
	line4 = pattern.sub('[email redacted]', line3)
	print line4,
	
wmtext.clock_on_right("10. Create deploy tracking file")
# create a 'random' number using UUID
# note that the last set of digits will correspond to the workstation
myUUID = str(uuid.uuid1())
tracking_filename = myUUID + ".txt"
target = open(tracking_filename, 'w')
target.write(myUUID + "\n")
target.write("Adam upload by Python script.\n")
target.write(gedcom_expected + "\n")
target.close()

wmtext.clock_on_right("11. Git -> commit and push")
#commit_msg = "Adam generated upload from " + gedcom_expected
os.chdir(github_folder)
print Fore.YELLOW + ' > git add -A' + Style.RESET_ALL
r1 = envoy.run('git add -A')
print r1.std_err,
print Fore.YELLOW + '> git commit -m Adam_upload' + Style.RESET_ALL
r2 = envoy.run('git commit -m Adam_upload')
print r2.std_out, r2.std_err,
print Fore.YELLOW + '> git push origin' + Style.RESET_ALL
r3 = envoy.run('git push origin')
print r3.std_out, r3.std_err

wmtext.clock_on_right("12. Wait to go live")
while True:
	r = requests.head(url_root + "/" + tracking_filename)
	if r.status_code == requests.codes.ok:
		break
	else:
		wmtext.wait(180)

wmtext.clock_on_right(Fore.GREEN + Style.BRIGHT + "Update is Live")
print Style.RESET_ALL	