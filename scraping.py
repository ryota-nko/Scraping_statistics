from collections import OrderedDict
from bs4 import BeautifulSoup
from urllib import request
import pandas as pd
import numpy as np
import sys

def transform( td , th , t , y ):
    global data_dic

    for h in th:
        if h.get_text() not in list( data_dic.keys() ):
            data_dic[h.get_text()] = []


    count = 0
    test = []
    for i,el in enumerate( td ):
        if count == 0:
            data_dic["大学"].append( t )
            data_dic["年度"].append( y )

        if count >= 8:
            count = 0
            data_dic["大学"].append( t )
            data_dic["年度"].append( y )


        data_dic[list( data_dic.keys() )[count+2]].append( str( el.get_text().replace('\u3000'," ") ) )
        count += 1


data_dic = OrderedDict()
data_dic["大学"] = []
data_dic["年度"] = []
year = np.arange( 2010 , 2020 , 1 )
season = [ "a" , "s" ]
team = ["W","K","M","H","T","R"]

for y in year:
    for s in season:
        for t in team:
            print( y , s , t )
            url = "https://www.big6.gr.jp/system/prog/team.php?s={}{}&t={}".format( y , s , t )

            response = request.urlopen(url)
            soup = BeautifulSoup(response , "html.parser")
            th = soup.find_all( "td" , rowspan="1" )
            td = soup.select( 'td[style*="height:27px;padding-top:7px;line-height:1.6em;"]' , limit=None )
            transform( td=td , th=th , t=t , y=y )
            response.close()




for key , value in data_dic.items():
    print( key , len( value ) )
df = pd.DataFrame.from_dict(data_dic)
df.to_csv("six_baseball_datas.csv")
