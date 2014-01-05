These are the html code pieces needed to make [Adam](http://timforsythe.com/tools/adam) run.

# Checklist for Website Generation

1. Export from RootsMagic
    * name file `William-yymmdd.ged`
	* Everyone, Notes, Sources, (no LDS information), Multimedia links, (ignore privatization options, we'll use Adam for that)

2. Clean-up GEDCOM export
    * (done by Adam) text replace ` DATE CALC ` with ` DATE CAL `
	* fix media file locations - regex - "S:\\Documents\\Genealogy\\[0-9]+[\.[a-z]+]*\.? " with "images\\"
	* move over new images
	
3. Upload to Adam

4. Configure Adam
    * update 'Updated' date in footer

5. Delete old Adam output (zip file) from GitHub folder
	
6. Download completed Adam output (zip file) & move it to GitHub folder

7. Delete old html files
    * `cd Documents\GitHub\genealogy`
	* `del *.html`

8. Unzip new Adam output
    * `"C:\Program Files\7-Zip\7z" e adam_xxx_xxxx.zip`
	
9. Replace Adam version in footer
    * use Notepad++ to do a replace in files
	
10. Replace index.html with customized version
    * `cp _adam\index.html .\index.html`
	
10. Git commit and push
    * `C:\Users\William\AppData\Local\GitHub\PortableGit_fed20eba68b3e238e49a47cdfed0a45783d93651\bin\git`
    * `git add .`
	* `git commit -m "commit message"`
	* `git push origin`