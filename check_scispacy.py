# Adapted from https://github.com/lubianat/ann/blob/main/prototypes/notebooks/scispacy_linking_via_umls.ipynb

import scispacy
import spacy
import pandas as pd
from wikidataintegrator import wdi_core
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker
from functools import lru_cache
import sys
from wikidata2df import wikidata2df
from mdutils.mdutils import MdUtils
import pandas as pd
import os.path
import rdflib
from datetime import date
import en_core_sci_sm

print("====== Loading ScispaCy ======")
nlp = en_core_sci_sm.load()

print("====== Setting AbbreviationDetector ======")
abbreviation_pipe = AbbreviationDetector(nlp)
nlp.add_pipe(abbreviation_pipe)

print("====== Setting EntityLinker ======")
linker = EntityLinker(resolve_abbreviations=True, name="umls")
nlp.add_pipe(linker)


# Function by github.com/lubianat with some slight alterations by github.com/jvfe
@lru_cache(maxsize=None)
def get_wikidata_item(wikidata_property, value):
    """Gets a Wikidata item for a determined property-value pair


      Args:
        property (str): The property to search
        value (str): The value of said property
      
      Returns:
        str: A Wikidata item or a "None" value if no item found.
    """
    query_result = wdi_core.WDItemEngine.execute_sparql_query(
        f'SELECT distinct ?item WHERE {{ ?item wdt:{wikidata_property} "{value}" }}'
    )
    try:
        match = query_result["results"]["bindings"][0]
    except:
        return None
    qid = match["item"]["value"]

    qid = qid.split("/")[4]
    return qid


def get_wdt_items_from_umls_entities(doc, wikidata=False):
    """Create a table from the UMLS entities and link them to WDT
    """
    identified = []
    for ent in doc.ents:
        print(ent)
        try:
            best_id = ent._.kb_ents[0][0]
        except IndexError:
            best_id = None
        print(best_id)
        identified.append([ent.text, ent.start_char, ent.end_char, best_id])

    entity_df = pd.DataFrame.from_records(identified, 
                                        columns=['label', 'start_pos', 'end_pos', 'umls_id'])
    
    if wikidata:
        entity_df['qid'] = entity_df['umls_id'].apply(lambda x: get_wikidata_item("P2892", x))

    return entity_df

def get_title_df(wd_id):
    query = """
    SELECT ?item ?itemLabel
    WHERE
    {
    VALUES ?item {wd:""" + wd_id + """}  
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """

    df = wikidata2df(query)
    
    return(df)

wd_id = sys.argv[1]

print("====== Getting title from Wikidata ======")

df = get_title_df(wd_id)
text = df["itemLabel"][0]
doc = nlp(text)

print("====== Ectracting UMLS entities ======")

print(get_wdt_items_from_umls_entities(doc))