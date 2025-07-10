#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from report import Report
import calendar
import re
import os

from stopwatch import StopWatch
from dbmanager import DBManager

class ReportManager():

    def __init__(self):
        
        self.watch = StopWatch()
        self.watch.start("init Report Manager")

        self.CurrentDir = os.path.dirname(os.path.abspath(__file__))
        
        self.db = DBManager() 
        self.db.Connect(self.CurrentDir + "/digikam4.db")
        
        self.report = Report()

        self.sql_images = 'from Images where Images.category = 1 and Images.status = 1'
        
        self.sql_join_imageinformation = '''
        from Images
        LEFT JOIN ImageInformation ON Images.Id = ImageInformation.ImageId
        where
        Images.status = 1
        and Images.category = 1
        '''
        
        self.sql_join_albums = '''
        from Images
        LEFT JOIN Albums ON Images.album = Albums.Id
        where
        Images.status = 1
        and Images.category = 1
        '''
        
        self.sql_join_imagemetadata = '''
        from Images
        LEFT JOIN ImageMetadata ON Images.Id = ImageMetadata.ImageId
        where
        Images.status = 1
        and Images.category = 1
        '''
        
        self.sql_join_imageinformation_imagemetadata = '''
        from
        Images
        LEFT JOIN ImageMetadata ON Images.Id = ImageMetadata.ImageId
        LEFT JOIN ImageInformation ON Images.Id = ImageInformation.ImageId
        where
        Images.status = 1
        and Images.category = 1
        '''
        
        self.sql_join_imageinformation_albums = '''
        from
        Images
        LEFT JOIN Albums ON Images.album = Albums.Id
        LEFT JOIN ImageInformation ON Images.Id = ImageInformation.ImageId
        where
        Images.status = 1
        and Images.category = 1
        '''
        
        self.sql_join_all = '''
        from
        Images
        LEFT JOIN ImageMetadata ON Images.Id = ImageMetadata.ImageId
        LEFT JOIN ImageInformation ON Images.Id = ImageInformation.ImageId
        LEFT JOIN Albums ON Images.album = Albums.Id
        where
        Images.status = 1
        and Images.category = 1
        '''
        
        self.sql_where_append = ''

        self.watch.stop("init Report Manager")
        
    def report_overview(self):
        
        self.watch.start("create Overview")
        
        self.report.clear_all()
        
        self.report.add_text("<h2>Welcome to Digikamstat!</h2><p>You can choose the Typ of Report in the List in the Toolbar above.</p>")
        
        #id for digikam internal tags for filtering out
        color_label_id = self.db.GetValueFromDB("select id from tags where name is \"Color Label None\";")
        pick_label_id = self.db.GetValueFromDB("select id from tags where name is \"Pick Label None\";")
        
        table = []
        table.append(["Key",  "Value"])
        table.append(["Photos", self.helper_get_image_count()])
        table.append(["Videos", self.db.GetValueFromDB("select count() as count from Images where Images.category = 2 and Images.status = 1;")])
        table.append(["Other Media", self.db.GetValueFromDB("select count() as count from Images where Images.category = 3 and Images.status = 1")])
        table.append(["Albums",  self.db.GetValueFromDB("select count() as count from Albums")])
        #- 2 beacouse of the 2 digikam internal tags "Color Label None" and "Pick Label None" which will be assigend automatically
        table.append(["Tags", self.db.GetValueFromDB("select count() as count from Tags") - 2])
        table.append(["Tags assigned", int(self.db.GetValueFromDB("select count() as count from ImageTags where tagid is not %s and tagid is not %s" % (color_label_id,  pick_label_id)))])
        table.append(["Printed area (10 x 15cm each Photo)", "%s m²" % round(float(self.helper_get_image_count())  * 10 * 15 / 10000, 2) ])
        table.append(["Stack height (1mm each Photo)", "%s m" % round(float(self.helper_get_image_count()) * 0.001, 2)])
        table.append(["Print costs (0,08€ each Photo)", "%s €" % round(float(self.helper_get_image_count()) * 0.08, 2)])
        table.append(["Viewing time (5sek each Photo)", "%s h" % round(float(self.helper_get_image_count()) * 5 / 60 / 60, 2)])
        
        self.report.add_table(table)

        self.watch.stop("create Overview")
        
        return self.report.get_report()
        
    def report_all(self):
        
        self.watch.start("create report all")
        
        self.sql_where_append = ''
        
        if(self.check_empty_report()):
            return self.report.get_report()
            
        self.report.clear_all()
        
        self.title = "the complete digikam database"
        
        #self.report.add_headline("<h2>Report for %s</h2>" % (title))
        
        self.report.add_tab("Time report for %s" % (self.title), 'timereport',  'Time Report')
        
        self.time_all()
        
        self.report.add_toplink()
        
        #self.report.add_headline("<h2>Charts for %s</h2>" % (title),  'topten',  'Top Ten')
        self.report.add_tab("Charts for %s" % (self.title),  'topten',  'Top Ten')
        
        self.topten_year()
        self.topten_month()
        self.topten_day()
        self.topten_album()
        
        self.report.add_toplink()
        
        self.report_photo()
        
        self.watch.stop("create report all")
        
        return self.report.get_report()
       
    def report_year(self,  year):
        
        self.watch.start("create report year")
        
        self.year = year
        self.sql_where_append = 'and substr(ImageInformation.creationDate,1,4) like "%s"' % (year)
        
        self.report.clear_all()
        
        if(self.check_empty_report()):
            return self.report.get_report()
            
        self.title = "the year %s" % (self.year)
        
        self.report.add_tab("Time report for %s" % (self.title),  'timereport',  'Time Report')
        
        self.time_year()
        
        self.report.add_toplink()
        
        self.report.add_tab("Charts for %s" % (self.title),  'topten',  'Top Ten')
        
        self.topten_month()
        self.topten_day()
        self.topten_album()
        
        self.report.add_toplink()
        
        self.report_photo()
                
        self.watch.stop("create report year")
        
        return self.report.get_report()
        
    def report_month(self,  year,  month):
        
        self.watch.start("create report month")
        
        self.year = int(year)
        self.month = int(month)
        self.sql_where_append = 'and substr(ImageInformation.creationDate,1,7) like "%s-%02d"' % (self.year, self.month)
        
        self.report.clear_all()
        
        if(self.check_empty_report()):
            return self.report.get_report()
            
        self.title = "the month %s/%s" % (self.month, self.year)
        
        self.report.add_tab("<h2>Time report for %s</h2>" % (self.title),  'timereport',  'Time Report')
        
        self.time_month()
        
        self.report.add_toplink()
        
        self.report.add_tab("Charts for %s" % (self.title),  'topten',  'Top Ten')
                
        self.topten_day()
        self.topten_album()
        
        self.report.add_toplink()
        
        self.report_photo()
        
        self.watch.stop("create report month")
        
        return self.report.get_report()

    def report_day(self,  year,  month,  day):
        
        self.watch.start("create report day")
        
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.sql_where_append = 'and substr(ImageInformation.creationDate,1,10) like "%s-%02d-%02d"' % (self.year, self.month, self.day)
        
        self.report.clear_all()
        
        if(self.check_empty_report()):
            return self.report.get_report()
            
        self.title = "the day %s.%s.%s" % (self.day, self.month, self.year)
        
        self.report.add_tab("<h2>Time report for %s</h2>" % (self.title),  'timereport',  'Time Report')
        
        self.time_day()
        
        self.report.add_toplink()

        self.report.add_tab("Charts for %s" % (self.title),  'topten',  'Top Ten')
        
        self.topten_album()
        
        self.report.add_toplink()
        
        self.report_photo()
        
        self.watch.stop("create report day")
        
        return self.report.get_report()

    def report_album(self, album):
        
        self.watch.start("create report album")
        
        self.album = album
        self.sql_where_append = 'and Albums.relativePath like "%s"' % (album)
        
        self.report.clear_all()
        
        if(self.check_empty_report()):
            return
            
        self.title = "the album %s" % (album)
        
        self.report.add_tab("<h2>Time report for %s</h2>" % (self.title),  'timereport',  'Time Report')
        
        self.time_album()
        
        self.report.add_toplink()
        
        self.report.add_tab("Charts for %s" % (self.title),  'topten',  'Top Ten')
        
        self.topten_day()
        
        self.report.add_toplink()
        
        self.report_photo()
        
        self.watch.stop("create report album")
        
        return self.report.get_report()
        
    def check_empty_report(self):
        summe = int(self.helper_get_current_image_count())
        
        if(summe == 0):
            self.report.add_text("<h3 class=\"warning\">No photos werer taken in this time!</h3>")
            return 1
            
    def helper_get_image_count(self):
        
        return int(self.db.GetValueFromDB("select count() as count %s;" % self.sql_images))
        
    def helper_get_current_image_count(self):
        
        return int(self.db.GetValueFromDB("select count() as count %s %s;" % (self.sql_join_imageinformation_albums,  self.sql_where_append)))
        
    def helper_get_min_year(self):
        
        return int(self.db.GetValueFromDB('''select substr(ImageInformation.creationDate, 1, 4)
        %s
        order by ImageInformation.creationDate ASC
		limit 1;
        ''' % self.sql_join_imageinformation))
        
    def helper_get_max_year(self):
        
        return int(self.db.GetValueFromDB('''select substr(ImageInformation.creationDate, 1, 4)
        %s
        order by ImageInformation.creationDate DESC
		limit 1;
        ''' % self.sql_join_imageinformation))
        
    def helper_get_album_list(self):
        
        return self.db.GetListFromDB("select relativePath as p from Images LEFT JOIN Albums ON Images.album = Albums.Id group by p order by p;")
        
    def time_all(self):
        
        summe = self.helper_get_image_count()
        
        # PHOTOS PER YEAR
        firstYear = self.helper_get_min_year()
        lastYear = self.helper_get_max_year()
        
        db_data = self.db.GetListFromDB('''select substr(ImageInformation.creationDate,1,4) as year, count() as count
            %s
            group by year order by year
            ''' % self.sql_join_imageinformation)
        
        db_dict = {}
        maxcount = 0
        
        for a in db_data:
            db_dict[a[0]] = a[1]
        
        graph = []
        table = []
        
        table.append(["Year", 
                            "Photos", 
                            "%"])
                            
        for a in range(firstYear,lastYear + 1):
            
            a = str(a)
            count = 0
            
            if a in db_dict:
                count = db_dict[a]
                # store the greatest number for graph creating
                maxcount = count if count > maxcount else maxcount
                
            table.append(["<a href=\"app://year/%s\">%s</a>" % (a, a), count,  "%.02f%%" % (float(count) / int(summe) * 100)])
                            
            graph.append([a,  count])
        
        table.append(["Average""", 
                            "%.02f" %(float(summe) / float(lastYear - firstYear)),  "%.02f%%" %(100 / float(lastYear - firstYear))])
                            
        table.append(["Sum""", 
                            summe, 
                            "100%"])

        self.report.add_hor_graph("Photos per Year", graph,  maxcount)
        self.report.add_table(table)
    
    def time_year(self):
        
        summe = self.helper_get_current_image_count()
        
        db_data = self.db.GetListFromDB("select substr(ImageInformation.creationDate,1,7) as month,count() as count %s %s group by month order by month;" % (self.sql_join_imageinformation, self.sql_where_append))
        
        db_dict = {}
        maxcount = 0
        
        for a in db_data:
            db_dict[a[0]] = a[1]
        
        graph = []
        table = []
        monthnames = ['January',  'February',  'March',  'April',  'May',  'June',  'July',  'August',  'September', 'Ocober',  'November',  'December']
        
        table.append(["Month", 
                            "Photos", 
                            "%"])
        
        for a in range(0,12):
            
            month = "%s-%02d" % (self.year,  a + 1)
            count = 0
            
            if month in db_dict:
                count = db_dict[month] 
                maxcount = count if count > maxcount else maxcount
                
            table.append(["<a href=\"app://month/%s\">%s</a>" % (month, monthnames[a]), count,  "%.02f%%" % (float(count) / int(summe) * 100)])
                            
            graph.append(["%02d" % (a + 1),  count])
        
        table.append(["Average""", 
                            "%.02f" %(float(summe) / 12.0),  "%.02f%%" %(100 / 12.0)])
                            
        table.append(["Sum""", 
                            summe, 
                            "100%"])

        self.report.add_hor_graph("Photos per month for %s" % (self.title), graph,  maxcount)
        self.report.add_table(table)      
    
    def time_month(self):
        
        summe = self.helper_get_current_image_count()
        
        db_data = self.db.GetListFromDB("select substr(ImageInformation.creationDate,1,10) as day,count() as count %s %s group by day order by day;" % (self.sql_join_imageinformation,  self.sql_where_append))
        
        db_dict = {}
        maxcount = 0
        
        for a in db_data:
            db_dict[a[0]] = a[1]
        
        graph = []
        table = []
       
        table.append(["Day", 
                            "Photos", 
                            "%"])
        
        weekday,  days = calendar.monthrange(int(self.year),  self.month)
        
        for a in range(1,days + 1):
            
            day = "%s-%02d-%02d" % (self.year, self.month, a)
            count = 0
            
            if day in db_dict:
                count = db_dict[day] 
                maxcount = count if count > maxcount else maxcount
                
            table.append(["<a href=\"app://day/%s\">%02d</a>" % (day, a), count,  "%.02f%%" % (float(count) / int(summe) * 100)])
                            
            graph.append(["%02d" % a,  count])
        
        table.append(["Average""", 
                            "%.02f" %(float(summe) / 12.0),  "%.02f%%" %(100 / 12.0)])
                            
        table.append(["Sum""", 
                            summe, 
                            "100%"])

        self.report.add_hor_graph("Photos per day for %s" % (self.title), graph,  maxcount)
        self.report.add_table(table) 
    
    def time_day(self):
        
        summe = self.helper_get_current_image_count()
        
        db_data = self.db.GetListFromDB("select substr(ImageInformation.creationDate,12,2) as hour,count() as count %s %s group by hour order by hour;" % (self.sql_join_imageinformation, self.sql_where_append))
        
        db_dict = {}
        maxcount = 0
        
        for a in db_data:
            db_dict[a[0]] = a[1]
        
        graph = []
        table = []
       
        table.append(["Hour", 
                            "Photos", 
                            "%"])
        
        for a in range(24):
            
            count = 0
            hour = "%02d" % (a)
            
            if hour in db_dict:
                count = db_dict[hour] 
                maxcount = count if count > maxcount else maxcount
                
            table.append([hour, count,  "%.02f%%" % (float(count) / int(summe) * 100)])
                            
            graph.append([hour,  count])
        
        table.append(["Average""", 
                            "%.02f" %(float(summe) / 24.0),  "%.02f%%" %(100 / 24.0)])
                            
        table.append(["Sum""", 
                            summe, 
                            "100%"])

        self.report.add_hor_graph("Photos per hour for %s" % (self.title), graph,  maxcount)
        self.report.add_table(table) 
    
    def time_album(self):
        
        summe = self.helper_get_current_image_count()
                
        db_data = self.db.GetListFromDB("select substr(ImageInformation.creationDate,1,10) as day,count(*) as count %s %s group by day order by day;" % (self.sql_join_imageinformation_albums, self.sql_where_append))
        
        graph = []
        table = []
        maxcount = 0
       
        table.append(["Day", 
                            "Photos", 
                            "%"])
        
        for a in db_data:
            
            count = a[1]
            maxcount = count if count > maxcount else maxcount
                
            table.append(["<a href=\"app://day/%s\">%s</a>" % (a[0], a[0]), count,  "%.02f%%" % (float(count) / int(summe) * 100)])
                            
            graph.append([a[0], count])
        
        table.append(["Average""", 
                            "%.02f" %(float(summe) / len(db_data)),  "%.02f%%" %(100 / len(db_data))])
                            
        table.append(["Sum""", 
                            summe, 
                            "100%"])

        self.report.add_hor_graph("Photos per day for %s" % (self.title), graph,  maxcount)
        self.report.add_table(table) 
        
    def report_photo(self):
        
        self.report.add_tab("Flash usage for %s" % (self.title),  'flash',  'Flash Usage')
        self.photo_flash()
        self.report.add_toplink()
        
        self.report.add_tab("ISO values for %s" % (self.title),  'iso',  'ISO values')
        self.photo_iso()
        self.report.add_toplink()
        
        self.report.add_tab("Focal Length values @35mm for %s" % (self.title),  'focal35mm',  'Focal length')
        self.photo_length()
        self.report.add_toplink()
        
        self.report.add_tab("Aperture Value for %s" % (self.title),  'aperture',  'Aperture')
        self.photo_aperture()
        self.report.add_toplink()

        self.report.add_tab("Shutter time Value for %s" % (self.title),  'shutter',  'Shutter Time')
        self.photo_time()
        self.report.add_toplink()
        
        self.report.add_tab("Camera make for %s" % (self.title),  'make',  'Camera make')
        self.photo_make()
        self.report.add_toplink()

        self.report.add_tab("Camera model for %s" % (self.title),  'model',  'Camera model')
        self.photo_model()
        self.report.add_toplink()

        self.report.add_tab("Lens model for %s" % (self.title),  'lens',  'Lens model')
        self.photo_lens()
        self.report.add_toplink()
    
    # START FLASH USAGE
    def photo_flash(self):
        
        flash = self.db.GetListFromDB("select ImageMetadata.flash & 1 as flash_out,count() %s and flash is not NULL %s group by flash_out order by flash_out; " % (self.sql_join_all,  self.sql_where_append)) 

        if(flash == None):
            self.report.add_text("<h3 class=\"warning\">No flash data for this time</h3>")
            return
            
        
        flash_fired = 0
        flash_not_fired = 0
        
        try:
            flash_not_fired = flash[0][1]
            
        except IndexError:
            print("flash[0][1] not present")
        
        try:
            flash_fired = flash[1][1]
            
        except IndexError:
            print("flash[0][1] not present")
            
        summe = self.helper_get_current_image_count()
        diff = int(summe - flash_fired - flash_not_fired)
        
        graph = []
        graph.append(["not fired", flash_not_fired])
        graph.append(["fired", flash_fired])
        graph.append(["no value", diff])
        
        maxcount = flash_not_fired if flash_not_fired > flash_fired else flash_fired
        maxcount = flash_not_fired if flash_not_fired > diff else diff
        
        self.report.add_hor_graph("Flash usage", graph,  maxcount)
        
        table = []
        
        table.append(["Flash status", 
                            "Photos", 
                            "%"])
        
        table.append(["Flash not fired",
                            flash_not_fired,
                            "%s %%" % (round(float(flash_not_fired) / summe * 100,  1))])
                            
        table.append(["Flash fired", 
                           flash_fired, 
                           "%s %%" % (round(float(flash_fired) / summe * 100,  1))])
                           
        table.append(["no value", 
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
        
        self.report.add_table(table)      
    
    # START ISO VALUE
    def photo_iso(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        
        table.append(["ISO Value",  "Photos",  "%"])
        
        ISOList = {
        0 : '1', 
        1 : '2', 
        2 : '4', 
        3 : '8', 
        4 : '16', 
        5 : '25',
        6 : '50', 
        7 : '100', 
        8 : '200', 
        9 : '400', 
        10 : '800', 
        11 : '1600', 
        12 : '3200', 
        13 : '6400', 
        14 : '12800', 
        15 : '25600',
        16 : '51200', 
        17 : '102400', 
        18 : '204800', 
        19 : '409600', 
        20 : '819200', 
        21 : '1638400'
        }
        
        iso = self.db.GetListFromDB("select CAST(round(log2(ImageMetadata.sensitivity) + 0.28) as INT) as log_iso, count() %s %s group by log_iso order by log_iso; " % (self.sql_join_all,  self.sql_where_append)) 
        
        if(iso == None):
            self.report.add_text("<h3 class=\"warning\">No ISO data for this time</h3>")
            return
        
        iso_dict = {}
        
        for row in iso:
            iso_dict[row[0]] = row[1]
            
        for key in ISOList:
            
            count = 0
            
            if(key in iso_dict):
                count = iso_dict[key]

            maxcount = count if count > maxcount else maxcount
            diff -= count
            table.append(["ISO %s" % (ISOList[key]),
                               count,
                               "%s %%" % (round(float(count) / summe * 100,  1))])
                               
            graph.append([ISOList[key],  count])
            
        table.append(["no value", 
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
        
        if(maxcount > 0):
            self.report.add_hor_graph("ISO values", graph,  maxcount)
            self.report.add_table(table)
        else:
            self.report.add_text("<h3 class=\"warning\">No ISO data for this time</h3>")
            
    def photo_length(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        
        table.append(["Focal Length",  "Photos",  "%"])
        
        LengthList = {
        0 : '1', 
        1 : '1', 
        2 : '1', 
        3 : '2', 
        4 : '3', 
        5 : '3', 
        6 : '4', 
        7 : '5', 
        8 : '7', 
        9 : '10', 
        10 : '12', 
        11 : '16', 
        12 : '20', 
        13 : '28',
        14 : '35', 
        15 : '50', 
        16 : '60', 
        17 : '75', 
        18 : '100', 
        19 : '135', 
        20 : '180', 
        21 : '220', 
        22 : '300', 
        23 : '350',
        24 : '500', 
        25 : '600', 
        26 : '800', 
        27 : '1000',
        28 : '1400'
        }
        
        length = self.db.GetListFromDB("select CAST(round(log(1.3, ImageMetadata.focalLength35)+ 0.5) as INT) as log_length, count() %s %s group by log_length order by log_length; " % (self.sql_join_all,  self.sql_where_append)) 
        
        if(length == None):
            self.report.add_text("<h3 class=\"warning\">No Focal length data for this time</h3>")
            return
            
        length_dict = {}
        
        for row in length:
            length_dict[row[0]] = row[1]
            
        for key in LengthList:
            
            count = 0
            
            if(key in length_dict):
                count = length_dict[key]

            maxcount = count if count > maxcount else maxcount
            diff -= count
            table.append(["%s mm" % (LengthList[key]),
                               count,
                               "%s %%" % (round(float(count) / summe * 100,  1))])
                               
            graph.append([LengthList[key],  count])
            
        table.append(["no value", 
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
        
        if(maxcount > 0):
            self.report.add_hor_graph("Focal Length", graph,  maxcount)
            self.report.add_table(table)      
        else:
            self.report.add_text("<h3 class=\"warning\">No Focal length data for this time</h3>")
    
    # START APERTURE VALUE
    def photo_aperture(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        table.append(["Aperture Value",  "Photos",  "%"])
        
        ApertureList = {
        0 : '1', 
        1 : '1,4', 
        2 : '2', 
        3 : '2,8', 
        4 : '4', 
        5 : '5.6', 
        6 : '8', 
        7 : '11', 
        8 : '16', 
        9 : '22', 
        10 : '32', 
        11 : '45', 
        12 : '64', 
        13 : '90'
        }
        
        aperture = self.db.GetListFromDB("select CAST(round(log(1.4, ImageMetadata.aperture)) as INT) as log_aperture, count() %s %s group by log_aperture order by log_aperture; " % (self.sql_join_all,  self.sql_where_append)) 
        
        if(aperture == None):
            self.report.add_text("<h3 class=\"warning\">No Aperture data for this time</h3>")
            return
            
        aperture_dict = {}
        
        for row in aperture:
            aperture_dict[row[0]] = row[1]
            
        for key in ApertureList:
            
            count = 0
            
            if(key in aperture_dict):
                count = aperture_dict[key]

            maxcount = count if count > maxcount else maxcount
            diff -= count
            table.append(["%s" % (ApertureList[key]),
                               count,
                               "%s %%" % (round(float(count) / summe * 100,  1))])
                               
            graph.append([ApertureList[key],  count])
            
        table.append(["no value", 
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
                           
        if(maxcount > 0):
            self.report.add_hor_graph("Aperture Value", graph,  maxcount)
            self.report.add_table(table)      
        else:
            self.report.add_text("<h3 class=\"warning\">No Aperture data for this time</h3>")

    def photo_time(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        table.append(["Time Value",  "Photos",  "%"])
        
        shuttertime_list = {
        -15 : '1/32000', 
        -14 : '1/16000', 
        -13 : '1/8000', 
        -12 : '1/4000', 
        -11 : '1/2000', 
        -10 : '1/1000', 
        -9 : '1/500', 
        -8 : '1/250', 
        -7 : '1/120', 
        -6 : '1/60', 
        -5 : '1/30', 
        -4 : '1/15', 
        -3 : '1/8', 
        -2 : '1/4', 
        -1 : '1/2', 
        0 : '1', 
        1 : '2', 
        2 : '4', 
        3 : '8', 
        4 : '15', 
        5 : '30', 
        6 : '60', 
        7 : '120', 
        8 : '240', 
        9 : '480', 
        10 : '960', 
        11 : '1920'
        }
        
        shuttertime = self.db.GetListFromDB("select CAST(round(log(2, ImageMetadata.exposureTime)) as INT) as log_shuttertime, count() %s %s group by log_shuttertime order by log_shuttertime; " % (self.sql_join_all,  self.sql_where_append)) 
        
        if(shuttertime == None):
            self.report.add_text("<h3 class=\"warning\">No Shutter time data for this time</h3>")
            return
            
        shuttertime_dict = {}
        
        for row in shuttertime:
            shuttertime_dict[row[0]] = row[1]
            
        for key in shuttertime_list:
            
            count = 0
            
            if(key in shuttertime_dict):
                count = shuttertime_dict[key]

            maxcount = count if count > maxcount else maxcount
            diff -= count
            table.append(["%s" % (shuttertime_list[key]),
                               count,
                               "%s %%" % (round(float(count) / summe * 100,  1))])
                               
            graph.append([shuttertime_list[key],  count])
            
        table.append(["no value", 
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
                           
        if(maxcount > 0):
            self.report.add_hor_graph("Time Value", graph,  maxcount)
            self.report.add_table(table)
        else:
            self.report.add_text("<h3 class=\"warning\">No Shutter time data for this time</h3>")

    def photo_make(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        table.append(["Make",  "Photos",  "%"])
        
        maker = self.db.GetListFromDB("select TRIM(make) as trim_make, count() as count %s %s and make is not NULL and make is not '' group by trim_make order by trim_make; " % (self.sql_join_all,  self.sql_where_append)) 
        makercounter = 0
        
        if(maker == None):
            self.report.add_text("<h3 class=\"warning\">No camera maker data for this time</h3>")
            return
            
        for i in (maker):

            saveData = self.report.escape_html(str(i[0]))
            
            if  (saveData == ''):
                continue
                
            makercounter += 1
            diff -= int(i[1])
            maxcount = int(i[1]) if int(i[1]) > maxcount else maxcount
            table.append(["%s) %s" % (makercounter, saveData), 
                                i[1],
                               "%s %%" % (round(float(i[1]) / summe * 100,  1))])
                               
            graph.append(["%s) " % (makercounter)
                                , i[1]])
            
        table.append(["no value",
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
        #graph.append(['no val',  diff])
        
        if(maxcount > 0):
            self.report.add_hor_graph("Camera make", graph,  maxcount)
            self.report.add_table(table)
        else:
            self.report.add_text("<h3 class=\"warning\">No camera maker data for this time</h3>")
        
    def photo_model(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        table.append(["Model",  "Photos",  "%"])
        
        model = self.db.GetListFromDB("select TRIM(model) as trim_model, count() as count %s %s and model is not NULL and model is not '' group by trim_model order by trim_model; " % (self.sql_join_all,  self.sql_where_append)) 
        
        if(model == None):
            self.report.add_text("<h3 class=\"warning\">No camera model data for this time</h3>")
            return
            
        modelcount = 0
        for i in (model):
            
            saveData = self.report.escape_html(str(i[0]))
            
            if  (saveData == ''):
                continue
                
            modelcount += 1
            diff -= int(i[1])
            maxcount = int(i[1]) if int(i[1]) > maxcount else maxcount
            table.append(["%s) %s" % (modelcount,saveData),
                                i[1],
                               "%s %%" % (round(float(i[1]) / summe * 100,  1))])
                               
            graph.append(["%s)" % (modelcount), i[1]])
            
        table.append(["no value",
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
        #graph.append(['no val',  diff])
        
        if(maxcount > 0):
            self.report.add_hor_graph("Camera model", graph,  maxcount)
            self.report.add_table(table)
        else:
            self.report.add_text("<h3 class=\"warning\">No camera model data for this time</h3>")
        
    def photo_lens(self):
        
        summe = self.helper_get_current_image_count()
        diff = summe
        
        graph = []
        table = []
        maxcount = 0
        table.append(["Lens",  "Photos",  "%"])
        
        lens = self.db.GetListFromDB("select TRIM(lens) as trim_lens, count() as count %s %s and lens is not NULL and lens is not '' group by trim_lens order by trim_lens; " % (self.sql_join_all,  self.sql_where_append)) 
        
        if(lens == None):
            self.report.add_text("<h3 class=\"warning\">No lens model data for this time</h3>")
            return
            
        #filter out lenses staring with numers (trash data)
        p = re.compile(r'^\d\d \d\d \d\d')
                    
        lenscount = 0
        for i in (lens):
            
            saveData = self.report.escape_html(str(i[0]))
           
            if p.match(saveData):
                continue
                
            lenscount += 1
            diff -= int(i[1])
            maxcount = int(i[1]) if int(i[1]) > maxcount else maxcount
            table.append(["%s) %s" % (lenscount,saveData),
                                i[1],
                               "%s %%" % (round(float(i[1]) / summe * 100,  1))])
                               
            graph.append(["%s)" % (lenscount), i[1]])
            
        table.append(["no value",
                           diff ,
                           "%s %%" % (round(float(diff)/ summe * 100,  1))])
        #graph.append(['no val',  diff])
        
        if(maxcount > 0):
            self.report.add_hor_graph("Lens model", graph,  maxcount)
            self.report.add_table(table)
        else:
            self.report.add_text("<h3 class=\"warning\">No lens model data for this time</h3>")
            
    #TOP TENS
    def topten_year(self):
        self.create_top_ten("year", "Year", "select substr(ImageInformation.creationDate,1,4) as year,count() as count %s group by year order by count desc limit 10;" % self.sql_join_imageinformation)
    
    def topten_month(self):
        self.create_top_ten("month", "Month", "select substr(ImageInformation.creationDate,1,7) as month,count() as count %s %s group by month order by count desc limit 10;" % (self.sql_join_imageinformation, self.sql_where_append))
        
    def topten_day(self):
        self.create_top_ten("day", "Day", "select substr(ImageInformation.creationDate,1,10) as day,count() as count %s %s group by day order by count desc limit 10;" % (self.sql_join_imageinformation_albums, self.sql_where_append))
        
    def topten_album(self):
        self.create_top_ten("album", "Album", "select Albums.relativePath as album,count() as count %s %s group by album order by count desc limit 10;" % (self.sql_join_imageinformation_albums, self.sql_where_append))

    def create_top_ten(self, typ, title, sql):

        db_data = self.db.GetListFromDB(sql)
        self.report.add_text("<h3>Photos per %s Top Ten</h3>" % title)
        table = []

        table.append([title, "Photos"])

        for a in db_data:
            table.append(["<a href=\"app://%(t)s/%(d)s\">%(d)s</a>" % {'t': typ, 'd': self.report.escape_html(str(a[0]))}, a[1]])
            
        self.report.add_table(table)
    
    def close_report(self):
        
        self.db.close_db()
