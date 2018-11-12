
# coding: utf-8

# In[28]:


import requests
from bs4 import BeautifulSoup
import pandas

base_url = "http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=00s="
r = requests.get(base_url + "0.html")
soup = BeautifulSoup(r.content, "html.parser")
pages = soup.find_all("a", {"class":"Page"})[-1].text

l=[]
for page in range(0,int(pages)*10,10):
    
    print(base_url + str(page) + ".html")
    r = requests.get(base_url + str(page) + ".html")
    soup = BeautifulSoup(r.content, "html.parser")
    properties = soup.find_all("div", {"class":"propertyRow"})
    
    for p in properties:
        d={}
        d["Price"] = p.find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")
        d["Address"] = p.find_all("span", {"class":"propAddressCollapse"})[0].text
        try:
            d["Locale"] = p.find_all("span", {"class":"propAddressCollapse"})[1].text
        except:
            d["Locale"] = None
            
        try:
            d["Beds"] = p.find("span", {"class":"infoBed"}).find("b").text
        except:
            d["Beds"] = None

        try:
            d["Area"] = p.find("span", {"class":"infoSqFt"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Full Baths"] = p.find("span", {"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = None

        try:
            d["Half Baths"] = p.find("span", {"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None

        lot_size = None
        for column_group in p.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class":"featureGroup"}),column_group.find_all("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text

        l.append(d)
        
df = pandas.DataFrame(l)
df.to_csv("Output.csv")

