#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import os
import sys
from wikidata2df import wikidata2df
from mdutils.mdutils import MdUtils
import pandas as pd
import os.path
import rdflib
from datetime import date

def main():
    def get_doi_df(wd_id):
        query = """
        SELECT ?item ?doi ?itemLabel
        WHERE
        {
        VALUES ?item {wd:""" + wd_id + """} .
        ?item wdt:P356 ?doi.  
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """

        df = wikidata2df(query)
        
        return(df)

    wd_id = sys.argv[1]
    doi_df = get_doi_df(wd_id)

    print(doi_df)
    if doi_df.empty == True:
        print("No DOI found for " + wd_id +".")
    else:
        base_url = "https://sci-hub.do/"+ doi_df["doi"].values[0]
        print(base_url)

        res = requests.get(base_url, verify=False)
        s = BeautifulSoup(res.content, 'html.parser')
        iframe = s.find('iframe')
        if iframe:
            url = iframe.get('src')
        
        filename = url.split("/")[-1].split("#")[0]
        filepath = "./downloads/" + filename

        os.system(f'wget -O {filepath} {url}' )
        os.system('xdg-open '+filepath + "&")




if __name__ == "__main__":
    main()


