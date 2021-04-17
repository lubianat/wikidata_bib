import os
import glob
import urllib.parse
import pandas as pd
import unicodedata


def render_dashboard(readings):

  url1 = get_query_url_for_articles(readings)
  url1_legend = "Articles read"
  url2 = get_query_url_for_topic_bubble(readings)
  url2_legend = "Topics of those articles (as bubbles)"
#  url3 = get_topics_as_table(readings)
#  url3_legend = "Map of institutions"
  url4 = get_query_url_for_venues(readings)
  url4_legend = "Most read journals "
  url5 = get_query_url_for_authors(readings) 
  url5_legend = "Authors of papers I've read"
  url6 = get_query_url_for_locations(readings)
  url6_legend =  "Map of institutions"
  url7 =  get_query_url_for_citing_authors(readings)
  url7_legend = "Map of institutions"


  license_statement = '''
            This content is available under a <a target="_blank" href="https://creativecommons.org/publicdomain/zero/1.0/"> 
            Creative Commons CC0</a> license.
  '''
  code_availability_statement = '''
  Source code for the website available at <a target="_blank" href="https://github.com/lubianat/wikidata_bib">
            https://github.com/lubianat/wikidata_bib </a>
  '''

  scholia_credit_statement = '''
SPARQL queries adapted from <a target="_blank" href="https://scholia.toolforge.org/">Scholia</a>
  '''

  creator_statement = '''
 Dashboard  by <a target="_blank" href="https://www.wikidata.org/wiki/User:TiagoLubiana">TiagoLubiana</a>
  '''

  site_title = "Wikidata Bib"
  site_subtitle = ''' Tiago Lubiana's personal reading status'''
  html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>""" + site_title + """</title>
  <meta property="og:description" content="powered by Wikidata">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link href="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
  <section class="section">
    <div class="container">
      <div class="columns is-centered">
        <div class="column is-half has-text-centered">
          <h1 class="title is-1"> """ + site_title + """</h1>
          <h2>""" + site_subtitle +"""</h2>
        </div>
      </div>
    </div>
    <div class="column is-half has-text-centered">
  </section>
   </section>

   <div role="navigation">
<ul class="nav nav-pills justify-content-center">
  <li class="nav-item">
    <a class="nav-link" aria-current="page" href="/wikidata_bib/">All time</a>
  </li>
    <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2020/November.html">November 2020</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2020/December.html">December 2020</a>
  </li>
    </li>
   <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2021/January.html">January 2021</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2021/February.html">February 2021</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2021/March.html">March 2021</a>
  </li>
   <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/this_week.html">This week</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/last_day.html">Last day</a>
  </li>
</ul>
</div>
      <h5 class="title is-5" style="text-align:center;"> """ + url1_legend + """</h5>
        <p align="center">
          <iframe width=75% height="400" src=""" + '"'+ url1 +'"' + """></iframe>
        </p>
    <br></br>
    <h5 class="title is-5" style="text-align:center;">""" + url2_legend + """ </h5>
        <p align="center">
        <iframe width=75%  height="400" src=""" + '"'+ url2 +'"' + """></iframe>
        </p>
        <br></br>
      <h5 class="title is-5" style="text-align:center;display:block;"> """ + url4_legend + """</h5>
                  <p align="center">
          <iframe width=75%   height="400" src=""" + '"'+ url4 +'"' + """></iframe>
          </p>
   <br></br>
      <h5 class="title is-5" style="text-align:center;"> """ + url5_legend + """  </h5>
        <p align="center">
            <iframe width=75%  height="400" src=""" + '"'+ url5+'"' + """></iframe>
        </p>
<br></br>
      <h5 class="title is-5" style="text-align:center;"> """ + url6_legend + """ </h5>
      <p align="center">
            <iframe width=75%  height="400" src=""" + '"'+ url6 +'"' + """></iframe>
      </p>
<br></br>
      <h5 class="title is-5" style="text-align:center;"> """ + url7_legend + """ </h5>
      <p align="center">
            <iframe width=75%  height="400" src=""" + '"'+ url7 +'"' + """></iframe>
      </p>
<br></br>
  </p>
  </div>
 </br>
  <footer class="footer">
    <div class="container">
      <div class="content has-text-centered">
        <p>""" + license_statement + """  </p>
        <p>""" + code_availability_statement + """ </p>
        <p>""" + scholia_credit_statement + """</p>
        <p>""" + creator_statement + """ </p>
      </div>
    </div>
  </footer>
</body>
</html>
  """
  return(html)


def render_url(query):
  return "https://query.wikidata.org/embed.html#" + urllib.parse.quote(query, safe='')
  
def get_query_url_for_articles(readings):
  query = """

  #defaultView:Table
  SELECT
  (MIN(?dates) AS ?date)
  ?work ?workLabel
  (GROUP_CONCAT(DISTINCT ?type_label; separator=", ") AS ?type)
  (SAMPLE(?pages_) AS ?pages)
  ?venue ?venueLabel
  (GROUP_CONCAT(DISTINCT ?author_label; separator=", ") AS ?authors)
  WHERE {
  VALUES ?work """ +  readings + """.
  ?work wdt:P50 ?author .
  OPTIONAL {
    ?author rdfs:label ?author_label_ . FILTER (LANG(?author_label_) = 'en')
  }
  BIND(COALESCE(?author_label_, SUBSTR(STR(?author), 32)) AS ?author_label)
  OPTIONAL { ?work wdt:P31 ?type_ . ?type_ rdfs:label ?type_label . FILTER (LANG(?type_label) = 'en') }
  ?work wdt:P577 ?datetimes .
  BIND(xsd:date(?datetimes) AS ?dates)
  OPTIONAL { ?work wdt:P1104 ?pages_ }
  OPTIONAL { ?work wdt:P1433 ?venue }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,no,ru,sv,zh". }  
  }
  GROUP BY ?work ?workLabel ?venue ?venueLabel
  ORDER BY DESC(?date)  

  """
  
  return render_url(query)

def get_query_url_for_topic_bubble(readings):

  query = """

  #defaultView:BubbleChart
  SELECT ?score ?topic ?topicLabel
  WITH {
    SELECT
      (SUM(?score_) AS ?score)
      ?topic
    WHERE {
          {
        SELECT (100 AS ?score_) ?topic WHERE {
          VALUES ?work """ +  readings + """.
          ?work  wdt:P921 ?topic . 
        }
      }
      UNION
      {
        SELECT (1 AS ?score_) ?topic WHERE {
          VALUES ?work """ +  readings + """.
          ?citing_work wdt:P2860 ?work .
          ?citing_work wdt:P921 ?topic . 
        }
      }
    }
    GROUP BY ?topic
  } AS %results 
  WHERE {
    INCLUDE %results
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,da,de,es,jp,no,ru,sv,zh". }
  }
  ORDER BY DESC(?score)
  LIMIT 50

  """
  return render_url(query) 

def get_topics_as_table(readings):
  query_3 = """


  #defaultView:Table
  SELECT ?count ?theme ?themeLabel ?example_work ?example_workLabel
  WITH {
    SELECT (COUNT(?work) AS ?count) ?theme (SAMPLE(?work) AS ?example_work)
    WHERE {
      VALUES ?work """ +  readings + """.
      ?work wdt:P921 ?theme .
    }
    GROUP BY ?theme
  } AS %result
  WHERE {
    INCLUDE %result
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh" . } 
  }
  ORDER BY DESC(?count) 

  """
  return render_url(query_3) 

def get_query_url_for_venues(readings):
  query_4 = """


  # Venue statistics for a collection
  SELECT
    ?count (SAMPLE(?short_name_) AS ?short_name)
    ?venue ?venueLabel
    ?topics ?topicsUrl
  WITH {
    SELECT
      (COUNT(DISTINCT ?work) as ?count)
      ?venue
      (GROUP_CONCAT(DISTINCT ?topic_label; separator=", ") AS ?topics)
    WHERE {
      VALUES ?work """ +  readings + """.
      ?work wdt:P1433 ?venue .
      OPTIONAL {
        ?venue wdt:P921 ?topic .
        ?topic rdfs:label ?topic_label . FILTER(LANG(?topic_label) = 'en') }
    }
    GROUP BY ?venue
  } AS %result
  WHERE {
    INCLUDE %result
    OPTIONAL { ?venue wdt:P1813 ?short_name_ . }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh". }  
  } 
  GROUP BY ?count ?venue ?venueLabel ?topics ?topicsUrl
  ORDER BY DESC(?count)

  """
  return render_url(query_4) 

def get_query_url_for_locations(readings):
  query_5 = """


  #defaultView:Map
  SELECT ?organization ?organizationLabel ?geo ?count ?layer
  WITH {
    SELECT DISTINCT ?organization ?geo (COUNT(DISTINCT ?work) AS ?count) WHERE {
      VALUES ?work """ +  readings + """.
          ?work wdt:P50 ?author .
      ?author ( wdt:P108 | wdt:P463 | wdt:P1416 ) / wdt:P361* ?organization . 
      ?organization wdt:P625 ?geo .
    }
    GROUP BY ?organization ?geo ?count
    ORDER BY DESC (?count)
    LIMIT 2000
  } AS %organizations
  WHERE {
    INCLUDE %organizations
    BIND(IF( (?count < 1), "No results", IF((?count < 2), "1 result", IF((?count < 5), "1 < results ≤ 10", IF((?count < 101), "10 < results ≤ 100", IF((?count < 1001), "100 < results ≤ 1000", IF((?count < 10001), "1000 < results ≤ 10000", "10000 or more results") ) ) ) )) AS ?layer )
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }        
  }
  ORDER BY DESC (?count)


  """
  return render_url(query_5)

def get_query_url_for_citing_authors(readings):
  query_6 = """


  #defaultView:Table
  SELECT
    ?count
    ?citing_author ?citing_authorLabel

    # Either show the ORCID iD or construct part of a URL to search on the ORCID homepage
    (COALESCE(?orcid_, CONCAT("orcid-search/quick-search/?searchQuery=", ENCODE_FOR_URI(?citing_authorLabel))) AS ?orcid)
  WITH {
    SELECT (COUNT(?citing_work) AS ?count) ?citing_author WHERE {
      VALUES ?work """ +  readings + """.
      ?citing_work wdt:P2860 ?work . 
      ?citing_work wdt:P50 ?citing_author .
    }
    GROUP BY ?citing_author 
    ORDER BY DESC(?count)
    LIMIT 500
  } AS %counts
  WITH {
    # An author might have multiple ORCID iDs
    SELECT
      ?count
      ?citing_author
      (SAMPLE(?orcids) AS ?orcid_)
    WHERE {
      INCLUDE %counts
      OPTIONAL { ?citing_author wdt:P496 ?orcids }
    }
    GROUP BY ?count ?citing_author
  } AS %result
  WHERE {
    INCLUDE %result

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh". }
  } 
  ORDER BY DESC(?count)


  """
  return render_url(query_6)

def get_query_url_for_authors(readings):
  query_7 = """
  #defaultView:Table
  SELECT (COUNT(?work) AS ?count) ?author ?authorLabel ?orcids  WHERE {
    VALUES ?work """ +  readings + """.
    ?work wdt:P50 ?author .
      OPTIONAL { ?author wdt:P496 ?orcids }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en,da,de,es,fr,jp,nl,no,ru,sv,zh". }

    }
  GROUP BY ?author ?authorLabel ?orcids 
  ORDER BY DESC(?count)

  """
  return render_url(query_7)
