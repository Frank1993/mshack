# -*- coding:utf-8 -*-

import sys

sys.path.append('../facepy/feature_extraction/')

#from facepy..image import extract_features

import extract_features
import pandas
import fnmatch
import os


#读取excel 文件并合并

similar_image_path = os.path.abspath('../data/image_similar/')
excel=pandas.read_excel(similar_image_path+'/1.xlsx')

for i in xrange(2,17):
    excel=excel.append(pandas.read_excel(similar_image_path+'/%s.xlsx'%i),ignore_index=True)

data=pandas.DataFrame({'id':excel[u'学号'],'name':excel[u'姓名'],'class':excel[u'班号'],'gender':excel[u'性别']})

def get_image_for_people(row):
    idOfPeople=row['id']
    imageName = None
    for file in os.listdir(similar_image_path):
        if fnmatch.fnmatch(file, '%s*.*'%idOfPeople):
            imageName=file
            break
    return imageName


print data
