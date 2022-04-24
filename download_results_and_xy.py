import urllib.request
import urllib.error
from pathlib import Path
import os

bp = Path(os.getcwd())

import pandas as pd
from pathlib import Path

def mkdir_except(folder_name):  # function to create folders and ignore if folder exists

    try:
        os.mkdir(folder_name)
        #print("Folder {} created. ".format(folder_name))

    except:
        print("Folder {} already exists. \n".format(folder_name))

def download_save_zip(url, folder_path):  # function for downloading url to a path

    file_name = url.split('/')[-1]
    sp = folder_path / file_name

    if os.path.isfile(sp):
        print("{} already downloaded \n".format(sp))

    else:
        try:
            req = urllib.request.urlopen(url)
            if not [i for i in req.getheaders() if 'text/html' in i]:
                print('Downloading: {} '.format(url))
                data = req.read()
                req.close()

                local = open(sp, 'wb')
                local.write(data)
                local.close()

        except urllib.error.HTTPError:
            print("HTTPError for {} ".format(url))

        except urllib.error.URLError:
            print("URLError for {} ".format(url))

# list of counties for scores to be run on. Below are counties within the 263m screening area
county_names = [
'Alameda',
'ContraCosta',
'DelNorte',
'Humboldt',
'LosAngeles',
'Marin',
'Mendocino',
'Monterey',
'Napa',
'Orange',
'Riverside',
'Sacramento',
'SanBenito',
'SanBernardino',
'SanDiego',
'SanFrancisco',
'SanLuisObispo',
'SanMateo',
'SantaBarbara',
'SantaClara',
'SantaCruz',
'Siskiyou',
'Solano',
'Sonoma',
'Trinity',
'Ventura'
]

date = input("Enter desired start date (YYYY-MM-DD): ")
edf_name = 'EDF.zip'
xy_name = 'GeoXY.zip'

# set base geotracker urls and create the path for geotracker downloads (edf AND xy)
geotracker_edf_url = "https://geotracker.waterboards.ca.gov/data_download/edf_by_county/"
geo_edf_path = bp / 'geotracker_edf_results'
mkdir_except(geo_edf_path)

geotracker_xy_url = "https://geotracker.waterboards.ca.gov/data_download/geo_by_county/"
geo_xy_path = bp / 'geotracker_xy'
mkdir_except(geo_xy_path)

def dl_geotracker(url_start, clist, url_alt, folder_path):

    urlList = []

    for i in clist:
        url = url_start + i + url_alt
        urlList.append(url)

    for j in urlList:
        download_save_zip(j, folder_path)

# runs download for geotracker sample resutls (edf) and xy locations
print('Downloading GeoTracker Data: \n')
dl_geotracker(geotracker_edf_url, county_names, edf_name, geo_edf_path)
dl_geotracker(geotracker_xy_url, county_names, xy_name, geo_xy_path)

# set base gama results url and creates a path for them to be downloaded to
gama_base_url = 'https://gamagroundwater.waterboards.ca.gov/gama/data_download/'
gama_res_path = bp / 'gama_results'
mkdir_except(gama_res_path)

# alternate url substrings for each dataset from GAMA
gama_alt_urls = [
    'ddw_',
    'dpr_',
    'dwr_',
    'gama_dom_',
    'gama_sp-study_',
    'gama_usgs_',
    'localgw_',
    'usgs_nwis_',
    'wb_cleanup_',
    'wb_ilrp_',
    'wrd_'
]

# gama results with dl_Save_zip()
def dl_gama_results(start_url, clist, alt_urls, dl_path):

    url_list = []

    pref = 'gama_'
    suf = '_v2.zip'

    for c in clist:
        c = c.lower()

        for au in alt_urls:
            url = start_url + pref + au + c + suf
            url_list.append(url)

    for url in url_list:
        download_save_zip(url, dl_path)


# Runs downloads for GAMA sample results
print('Downloading GAMA sample results: \n')
dl_gama_results(gama_base_url, county_names, gama_alt_urls, gama_res_path)

# set base GAMA xy url and path for downloads
gama_xy_url = 'https://gamagroundwater.waterboards.ca.gov/gama/data_download/gama_location_construction_v2.zip'
gama_xy_path = bp / 'gama_xy'
mkdir_except(gama_xy_path)

# runs download for GAMA xy data
print('Downloading GAMA XY data: \n')
gama_xy = download_save_zip(gama_xy_url, gama_xy_path)