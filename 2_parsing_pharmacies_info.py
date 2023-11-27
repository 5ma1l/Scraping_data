from ville import villes
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse, parse_qs
import pandas as pd
import time

import time

def wait_responce(url):
    timeout_seconds = 10  # Adjust this value based on your requirements

    start_time = time.time()
    content=None
    while True:
        # Make the request
        response = requests.get(url)
        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            content = response.content
            break  # Exit the loop if the response is successful
        elif time.time() - start_time > timeout_seconds:
            print("Timeout reached. Exiting.")
            break  # Exit the loop if the timeout is reached
        else:
            print(f"Waiting for response. Status code: {response.status_code}")
            time.sleep(1)  # Wait for 1 second before checking again
    return content

url="https://www.annuaire-gratuit.ma"

data = {
    'id': [],
    'title': [],
    'Adresse': [],
    'Ville': [],
    'Pays':[],
    'Thématique':[],
    'N° Téléphone': [],
    'Location':[],
    'Référence':[],
    'worktime':[]
}

id=0

for i in range(len(villes)):
    link_ville=villes[i]['link']
    content=wait_responce(url+link_ville)

    bs=BeautifulSoup(content,'html.parser')
    pharmacie=bs.find_all('a')
    links_pharmacies=[]

    for phar in pharmacie:
        link=phar.get('href')
        if link != None and '/pharmacie-' == link[:11] and 'garde'!=link[11:11+5]:
            links_pharmacies.append(link)
    print(links_pharmacies)
    
    for j in range(len(links_pharmacies)):
        
        pharmacie=links_pharmacies[j]
        content=wait_responce(url+pharmacie)
        bs=BeautifulSoup(content,"html.parser")
        title=bs.find('h1')
        if title!=None:
            tables=bs.find_all('tbody')

            cols=[t.find_all('tr') for t in tables]
            if len(cols)>=2:
                
                data['id'].append(i)

                data['title'].append(title.getText())

                for c in cols[0]:
                    values=c.find_all('td')
                    value=[v.get_text() for v in values]
                    if value[0]=='N° Téléphone':
                        value[1]=''.join(re.findall(r'\d+',value[1]))
                    elif value[0]=='Adresse':
                            url_map=c.find('a').get('href')
                            if url_map!='':
                                parsed_url = urlparse(url_map)
                                # Extract the values of 'l' and 'q' parameters
                                query_params = parse_qs(parsed_url.query)
                                c_value = query_params.get('q', [None])[0]
                                data['Location'].append(c_value)
                            else:
                                data['Location'].append('')
                    if value[0] in data.keys():
                        data[value[0]].append(value[1])

                histoires=cols[1]

                keys=[n.get_text() for n in histoires[1].find_all('th')]
                res1=[]
                for h in histoires[2:-1]:
                    info={}
                    values=[m.get_text() for m in h.find_all('td')]
                    for k in range(len(keys)):
                        if len(values)>k:
                            info[keys[k]]=values[k]
                        else:
                            info[keys[k]]=''
                    res1.append(info)

                data['worktime'].append(res1)
                id+=1
                print(id)

with open('data.txt','w') as f:
    f.write(str(data))
