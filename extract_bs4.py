import requests
import logging
from bs4 import BeautifulSoup
import pandas as pd

from progress.bar import Bar

# select rows by background colors
target_colors = ["#f4f4ff", "#ffffff" ] 

def extract_data_from_url(url, year):
    # call URL and get markdown 
    src = requests.get( url)
    soup = BeautifulSoup(src.content, 'html.parser')
    # objs = list(soup.children)[2]
    #print('extracting data from..', url)
    # get all the table rows
    rows = soup.find_all("tr")

    obj_list = []

    count = 0
    for r in rows:
        if 'bgcolor' in r.attrs:
            #print(f'@{count}={obj["bgcolor"]}')
            for c in target_colors:
                if c == r.attrs['bgcolor']:
                    insert = {
                        'studio': '', 
                        'gross': '',
                        'num_theaters': '',
                        'opening': '',
                        'open': '',
                        'close':''
                    }

                    try:
                        insert['studio'] = r.contents[2].contents[0].contents[0].contents[0],
                        insert['gross'] = r.contents[3].contents[0].contents[0].contents[0],
                        insert['num_theaters'] = r.contents[4].contents[0].contents[0],
                        insert['opening'] =   r.contents[5].contents[0].contents[0],
                        insert['open'] =   r.contents[7].contents[0].contents[0].contents[0],
                        
                       
                    except:
                        break
                     

                    # most movies have a valid hyperlink
                    try:
                        insert['title'] = r.contents[1].contents[0].contents[0].contents[0].contents[0]
                    except:
                        #print('no hyperlink found!')
                        # but if they don't it will just be text
                        insert['title'] = r.contents[1].contents[0].contents[0].contents[0]
                        pass

                    try:
                        insert['close'] = r.contents[8].contents[0].contents[0]

                    except:
                        # set to default from website, cleanup in transform step later
                        insert['close'] = '-'
                        pass
                    insert['year'] = year
                    obj_list.append(insert)
                    #print( f'inserted @ {count}! {insert["title"]}' )
                        
        #s print("@", r.attrs["'bgcolor'"])
        count += 1
        if count > 108:
            #print('at end of rows... break!')
            break

    df = pd.DataFrame(obj_list)
    return df

def get_urls_for_year(year):
    base_url = 'https://www.boxofficemojo.com/yearly/chart/'

    

    # https://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2019&p=.htm'
    bounce_back = False
    page = 1 
    urls = []
    while bounce_back==False:
        #https://www.boxofficemojo.com/yearly/chart/?yr=2018&p=.htm
        url_with_page = f"{base_url}?page={page}&yr={year}"
        #print(f'going to {url_with_page}')
        r = requests.get(url_with_page)
        if r.status_code != 200:
            bounce_back = True
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            # get all the table rows
            rows = soup.find_all("tr")

            if len(rows) < 7 :
                 bounce_back = True
                 break
            #print('tr count: ', len(rows))
            page+=1
            urls.append( url_with_page )
    
    #print(f'total pages for {year} = {len(urls)}')
    return urls


urls = []

year_bar = Bar(f'paginating years ', max=(2020-1980))

years = []
for year in range (1980,2020):
    pages = get_urls_for_year(str(year))
    year_bar.next()
    for page in pages:
        urls.append(page)
        years.append(year)
year_bar.finish()

df = pd.DataFrame()

bar = Bar(f'extracting box office data data', max=len(urls))

for index in range(0,len(urls)):
    _df = extract_data_from_url(urls[index], years[index])
    bar.next()
    df = df.append(_df, ignore_index=True)
bar.finish()
print('length of DF: ', len(df))

df.to_csv('./export/movies.csv', index=False)
print('debugger')