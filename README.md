# digikamstat
A report tool for your photos managed in digikam

The tool uses the information stored in the digikam database to produce various reports.\
It will show you
- how many photos per year/month/day/album were created
- how the photographic settings (e.g. focal length, aperture, shuter time) are distributed in the given time frame/album
- which was the day were the most photos are taken

It will not alter the photos or the database file.

## Installation

- Make sure you have the pysid6 and sqlite3 packages for python installed
- download digikamstat release
- extract the archive file
- copy the file digikam4.db from your digikam folder to the folder where the script is stored
- run the script digikamstat.py (it's possible that you have to set the execution permiission on the file)
- or run it from the konsole 
 - change to the directory you have extracted the archive
 - run python (or python3) ./digikamstat.py
 
## Usage

On startup you will see the overall statistics for your photos managed in digikam.\
On the top toolbar you can choose the report type you want to generate and the press the "Report!" button to create the chosen report type.\
Once the report is created, in some tables you can click on the blue links to create the report for that link.

The script will create the current report as report.xhtml file in the script directory. Youn can archive the files or print them.

The print function will generate a report.pdf file in the script directory, but the file is currently broken and shows only the first tab of data.

## Problems

Known problem s
- The printed pdf file contains only the first tab from the report window. I have to make the printing css work in chromium.
- The tables for e.g. focal length need a bit or rework (e.g. 3 times 1mm in the table)

This is the first release of digikamstat. If you have any problems, please kontact me (digikamstat@tobbegraf.de).\
If possible, please start the script from the command line and share the output with me for troubleshooting.

## Screenshots

### digikamstat window with overall report
![digikamstat window with overall report](/screenshots/mainwindow1.png?raw=true "digikamstat window")

### digikamstat window with time report for the year 2024
![digikamstat window with time report for the year 2024](/screenshots/mainwindow2.png?raw=true "digikamstat window")

### digikamstat window with report about the aperture values for the year 2024
![digikamstat window with report about the aperture values for the year 2024](/screenshots/mainwindow3.png?raw=true "digikamstat window")

### digikamstat window with report about the used camera models for the year 2024
![digikamstat window with report about the aperture values for the year 2024](/screenshots/mainwindow4.png?raw=true "digikamstat window")

### digikamstat window with report for a single day 
![digikamstat window with report about the used camera models for the year 2024](/screenshots/mainwindow5.png?raw=true "digikamstat window")

### digikamstat window with report with top ten charts
![digikamstat window with report with top ten charts](/screenshots/mainwindow6.png?raw=true "digikamstat window")
