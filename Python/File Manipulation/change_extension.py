import os
import glob

files = glob.glob('*.jpg,')
for file in files:
    os.rename(file, '{}'.format(file.split(',')[0]))
