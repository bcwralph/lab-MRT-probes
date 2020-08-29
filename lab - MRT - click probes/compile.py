import os,sys
import string
#import pygame

source_1 = "data"

append_sart = open("appended_data.xls","w")

for i in os.listdir(source_1):
    sf = open(source_1+'/'+i,'r')
    header = sf.readline()
    line = sf.readline()
    while line != '':
        append_sart.write(line)
        line = sf.readline()
    sf.close()

append_sart.flush()
append_sart.close()
