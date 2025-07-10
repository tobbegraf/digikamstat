# #!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sqlite3
from stopwatch import StopWatch

class DBManager():
    
    #borg design from http://code.activestate.com/recipes/66531/
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
        #because the constructor is called every time and the cache would then be deleted
        if not 'watch' in dir(self):
            self.watch = StopWatch()
            self.cache = {}
    
    def __call__(self):
        return self

    def Connect(self,  dbname):
        if(os.path.isfile(dbname)):
            self.conn = sqlite3.connect(dbname)
            self.cur = self.conn.cursor()
            self.cur.execute('PRAGMA query_only=1;')
            return True
        else:
            print("Connot connect to Databse: %s" % dbname);
            return False
        #self.prepareDB()
        
#    def prepareDB(self):
#         self.watch.start('prepare db, create view')
#         self.cur.execute('drop table if exists digikamstat;')
#         self.cur.execute('PRAGMA cache_size=10000;')
#         self.cur.execute('PRAGMA synchronous=OFF;')
#         self.cur.execute('PRAGMA count_changes=OFF;')
#
#
#         self.cur.execute('''create temp table digikamstat (
#             id INTEGER,
#             albumid INTEGER,
#             album TEXT,
#             creationDate TEXT,
#             year TEXT,
#             month TEXT,
#             day TEXT,
#             hour TEXT,
#             make TEXT,
#             model TEXT,
#             lens TEXT,
#             exposureTime REAL,
#             aperture REAL,
#             focalLength35 REAL,
#             sensitivity INTEGER,
#             flash INTEGER)
#             ;''')
#
#         self.cur.execute('''create Index tmpid on digikamstat(id);''')
#         self.cur.execute('''create Index tmpalbumid on digikamstat(albumid);''')
#         self.cur.execute('''create Index tmpalbum on digikamstat(album);''')
#         self.cur.execute('''create index tmpcreationdate on digikamstat(creationDate);''')
#         self.cur.execute('''create Index tmpyear on digikamstat(year);''')
#         self.cur.execute('''create Index tmpmonth on digikamstat(month);''')
#         self.cur.execute('''create Index tmpday on digikamstat(day);''')
#         self.cur.execute('''create Index tmphour on digikamstat(hour);''')
#         self.cur.execute('''create Index tmpmake on digikamstat(make);''')
#         self.cur.execute('''create Index tmpmodel on digikamstat(model);''')
#         self.cur.execute('''create Index tmplens on digikamstat(lens);''')
#         self.cur.execute('''create Index tmpexposureTime on digikamstat(exposureTime);''')
#         self.cur.execute('''create Index tmpaperture on digikamstat(aperture);''')
#         self.cur.execute('''create Index tmpfocalLength35 on digikamstat(focalLength35);''')
#         self.cur.execute('''create Index tmpsensitivity on digikamstat(sensitivity);''')
#         self.cur.execute('''create Index tmpflash on digikamstat(flash);''')
#
#         self.cur.execute('''insert into digikamstat
#             select
#             Images.id as id,
#             Images.album as albumid,
#             Albums.relativePath as album,
#             ImageInformation.creationDate as creationDate,
#             substr(ImageInformation.creationDate,1,4) as year,
#             substr(ImageInformation.creationDate,1,7) as month,
#             substr(ImageInformation.creationDate,1,10) as day,
#             substr(ImageInformation.creationDate,12,2) as hour,
#             TRIM(ImageMetadata.make) as make,
#             TRIM(ImageMetadata.model) as model,
#             TRIM(ImageMetadata.lens) as lens,
#             ImageMetadata.exposureTime as exposureTime,
#             ImageMetadata.aperture as aperture,
#             ImageMetadata.focalLength35 as focalLength35,
#             ImageMetadata.sensitivity as sensitivity,
#             ImageMetadata.flash & 1 as flash
#             from
#             Images
#             LEFT JOIN ImageMetadata ON Images.Id = ImageMetadata.ImageId
#             LEFT JOIN ImageInformation ON Images.Id = ImageInformation.ImageId
#             LEFT JOIN Albums ON Images.album = Albums.Id
#             where
#             Images.status = 1
#             and Images.category = 1;
#             ''')
#
#         self.watch.stop('prepare db, create view')
        
    def GetValueFromDB(self, query):
        
        query = query.strip()
        
        self.watch.start(query)
        
        if query not in self.cache:
            
            self.cur.execute(query)
            self.cache[query] = self.cur.fetchone()[0]
                
        else:
            print("cached!")
        
        self.watch.stop(query)
        return self.cache[query]
        
    def GetListFromDB(self, query):
        
        query = query.strip()
        
        self.watch.start(query)
        
        if query not in self.cache:
            
            self.cur.execute(query)
            self.cache[query] = self.cur.fetchall()
            
        self.watch.stop(query)
        return self.cache[query]
    
    def close_db(self):
        
        print("closing db")
        self.conn.close()
