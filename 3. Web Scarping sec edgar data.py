'''

This script is written to analyse URECA_sec edgar data
By Chan Wen Le 9/2019

'''

import urllib
import time 
import csv 
import sys  
from bs4 import BeautifulSoup
import pandas as pd

#specify file location
file_loc='C:/Users/Wen Le/Desktop/URECA (2)/'
base_index_url='https://www.sec.gov/Archives/edgar/full-index/'
base_report_url = 'https://www.sec.gov/Archives/'

#specify interested date range
years=range(2018,2019)
qtrs=['QTR1','QTR2','QTR3','QTR4']

#specify intrested form type
form_type='10-K'

#specify interested taregt word
target_word='Blockchain'

# for every year & qtr, get a record of all 10-k report
for year in years:
    for qtr in qtrs:
        filename='_'+year+qtr
        qtr_records=pd.DataFrame()
        print(filename)
        response=urllib.request.urlopen(base_index_url+year+'/'+qtr+'/form.idx')
        html_return = response.read()
        temp=[]
        for line in html_return.decode('utf-8').split('\n'):
            temp.append(line.split())
        for record in temp:
            try:
                if record[0]==form_type:
                   qtr_records=qtr_records.append({'Company Name':record[1:-3],'SIC':record[-3],'Date':record[-2],'Link':record[-1]},ignore_index=True)
            except IndexError:
                continue
        qtr_records.to_csv(file_loc+filename+'.csv')

        # then for each record, do a search & count of target word
        #here we can get other regex serach to find other information eg sic
                    print(i, end =',')
                    try:
                        soup=BeautifulSoup(urllib.request.urlopen(base_report_url+row['Link']), "lxml")
                        all_text=soup.get_text()
            #could have just used count but count is case sentitive, so use reegx instead
                        qtr_records.loc[i,'Count of '+target_word]=len(re.findall(target_word,all_text,re.IGNORECASE))
                        
            #search for SIC
                        match= re.search('STANDARD INDUSTRIAL CLASSIFICATION::(.*)', all_text[:1000], re.IGNORECASE)
                        if match:
                            grp=(re.sub('\s', '',match.group(1)))
                            _2019qtr1.loc[i,'SIC']=re.search('\[(.*?)\]',grp).group()[1:-1]        
                        else:
                            _2019qtr1.loc[i,'SIC']='NOT FOUND'
                        
                    except:
                        qtr_records.to_csv('error.csv')
                        print('error')
                        continue
        #only keeo those company list with target word>0
        qtr_records=qtr_records[qtr_records['Count of '+target_word]>0]
        qtr_records.to_csv(year+qtr+'.csv',index=False)



