#!usr/bin/python
import urllib.request
from bs4 import BeautifulSoup
import pymongo
import time

# Regions
regions = ['Arusha', 'Dar es Salaam', 'Dodoma', 'Iringa', 'Kagera', 'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara',
           'Mbeya', 'Morogoro', 'Mtwara', 'Mwanza', 'Pwani', 'Rukwa', 'Ruvuma', 'Shinyanga', 'Singida', 'Tabora',
           'Tanga']

# Districts
Arusha = ['Arumeru', 'Arusha', 'Karatu', 'Longido', 'Monduli', 'Ngorogoro']
Dar_es_Salaam = ['Ilala', 'Kinondoni', 'Temeke']
Dodoma = ['Bahi', 'Buigiri', 'Chamwino', 'Dodoma', 'Dodoma+(V)', 'Kondoa', 'Kongwa', 'Mpwapwa']
Iringa = ['Iringa', 'Iringa+(V)', 'Kilolo', 'Ludewa', 'Makete', 'Mufindi', 'Njombe']
Kagera = ['Biharamulo', 'Bukoba', 'Bukoba+(V)', 'Chato', 'Kahama', 'Karagwe', 'Misenyi', 'Muleba', 'Ngara']
Kigoma = ['Kasulu', 'Kibondo', 'Kigoma', 'Kigoma+(V)']
Kilimanjaro = {'Hai', 'Himo', 'Moshi', 'Moshi+(V)', 'Mwanga', 'Rombo', 'Same', 'Siha'}
Lindi = ['Kilwa', 'Lindi', 'Lindi+(V)', 'Liwale', 'Nachingwea', 'Ruangwa']
Manyara = ['Babati', 'Babati+(V)', 'Hanang', 'Kiteto', 'Manyara', 'Mbulu', 'Simanjiro']
Mara = ['Bunda', 'Musoma', 'Musoma+(V)', 'Rorya', 'Serengeti', 'Tarime']
Mbeya = ['Chunya', 'Ileje', 'Kyela', 'Mbarali', 'Mbeya', 'Mbeya+(V)', 'Mbozi', 'Rujewa', 'Rungwe']
Morogoro = ['Ifakara', 'Kilombero', 'Kilosa', 'Mahenge', 'Morogoro', 'Morogoro+(V)', 'Mvomero', 'Ulanga']
Mtwara = ['Masasi', 'Mtwara', 'Mtwara+(V)', 'Namtumbo', 'Newala', 'Tandahimba']
Mwanza = ['Geita', 'Ilemela', 'Kwimba', 'Magu', 'Misungwi', 'Mwanza', 'Mwanza+(V)', 'Nyamagana', 'Sengerema', 'Ukerewe']
Pwani = ['Bagamoyo', 'Kibaha', 'Kisarawe', 'Mafia', 'Mkuranga', 'Rufiji']
Rukwa = ['Mpanda', 'Mpanda+(V)', 'Nkasi', 'Sumbawanga', 'Sumbawanga+(V)']
Ruvuma = ['Mbinga', 'Namtumbo', 'Ruvuma', 'Songea', 'Songea+(V)', 'Tunduru']
Shinyanga = ['Bariadi', 'Bukombe', 'Kahama', 'Kishapu', 'Maswa', 'Meatu', 'Shinyanga', 'Shinyanga+(V)']
Singida = ['Iramba', 'Manyoni', 'Singida', 'Singida+(V)']
Tabora = ['Igunga', 'Nzega', 'Sikonge', 'Tabora', 'Tabora+(V)', 'Urambo', 'Uyui']
Tanga = ['Handeni', 'Kilindi', 'Korogwe', 'Lushoto', 'Mkinga', 'Muheza', 'Pangani', 'Tanga']

try:
    conn = pymongo.MongoClient()
    print("Connected to Mongo.")
    print('')
except Exception as e:
    print("Couldn't connect to Mongo: " + str(e))
    time.sleep(4)
    conn = pymongo.MongoClient()
    print("Connected to Mongo.")
    print('')


# Mongo db creation and writing function
def mongodb(data):
    print('Creating a database:')
    print('.......')
    db = conn.primary

    print('Creating a collection:')
    print('..........')
    collection = db.primary_schools

    print('Inserting data info mongo:')
    print('..........')
    collection.insert_many(data)

    print("Finished writing on collection 'primary'.")
print('')


# Scraping and saving to db funcion ..
def scrape(urls):
    print('Opening the urls for parsing')
    print('......')
    try:
        # req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        # use above if the site blocks or refuses your connection(when using urllib.request)
        r = urllib.request.urlopen(urls)
    except:
        time.sleep(4)
        r = urllib.request.urlopen(urls)

    print('Reading the page')
    print('............')
    html = r.read()

    print('Creating our soup')
    print('............')
    soup = BeautifulSoup(html, 'lxml')

    td = {}

    tables = soup.findAll('table')

    print('parsing through our data and taking the needed')
    print('.........')
    for i in range(len(tables)):
        table_rows = tables[i].select('tr')

        td['Name'] = table_rows[0].findAll('td')[0].text.strip()

        td['Type'] = table_rows[2].findAll('td')[0].text.strip()

        td['District'] = table_rows[3].findAll('td')[2].text.strip()

        td['Region'] = table_rows[4].findAll('td')[2].text.strip()

        print('Data extracted is:')
        print('')
        print('{0}, {1}'.format(td['Name'], td['Type']))
        print('{0}, {1}'.format(td['Region'], td['District']))
        print('')

        print('Entering scraped data to our database:')
        print('...........')
        mongodb(td)
        print('Finished writing to db.')
        print('')


# Checks the total results in each page n calculates amount of pages
def pagnum(urls):
    try:
        # req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        # use above if the site blocks or refuses your connection(when using urllib.request)
        r = urllib.request.urlopen(urls)
    except:
        time.sleep(4)
        r = urllib.request.urlopen(urls)

    html = r.read()

    soup = BeautifulSoup(html, 'lxml')

    results = soup.findAll('b')

    total_schools = int(results[1].text)

    print('Opening the page and getting page no for total pages to parse')
    print('........')
    if total_schools < 10:
        pageno = 1
    elif total_schools == 0:
        pass
    else:
        pagenum = round(int(results[1].text) / 10)

        pageno = pagenum + 1

    print('Total pages to parse in this area are: ' + str(pageno))
    print('')
    return pageno

# Main loop
for region in regions:
    print('Starting scraping: ')
    print('..........')
    if region is regions[0]:
        for district in Arusha:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)
            
    if region is regions[1]:
        daregion = 'Dar+es+Salaam'
        for district in Dar_es_Salaam:
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + daregion + "&district=" + district
            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + daregion + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[2]:
        for district in Dodoma:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[3]:
        for district in Iringa:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[4]:
        for district in Kagera:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[5]:
        for district in Kigoma:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[6]:
        for district in Kilimanjaro:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[7]:
        for district in Lindi:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[8]:
        for district in Manyara:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[9]:
        for district in Mara:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[10]:
        for district in Mbeya:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[11]:
        for district in Morogoro:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[12]:
        for district in Mtwara:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[13]:
        for district in Mwanza:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[14]:
        for district in Pwani:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[15]:
        for district in Rukwa:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[16]:
        for district in Ruvuma:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[17]:
        for district in Shinyanga:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[18]:
        for district in Singida:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[19]:
        for district in Tabora:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)

    if region is regions[20]:
        for district in Tanga:
            # urls = []
            urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                1) + "&region=" + region + "&district=" + district

            for pgno in range(pagnum(urls)):
                # urls = []
                urls = "http://www.schoolsinfo.co.tz/?SchType=primary&Page=" + str(
                        pgno + 1) + "&region=" + region + "&district=" + district
                # print(urls)
                scrape(urls)
                time.sleep(1)
            print('Finishing some things.')
            print('Now exiting......')
            raise SystemExit('Done.!')
