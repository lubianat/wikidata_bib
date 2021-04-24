# Wikidata Bib Manager v0

This repo is a propotype for bibliography management using Wikidata. 

The overarching goal is to leverage linked open data to navigate your studies and personal notes. 

You can check some queries on my notes at [lubianat.github.io/wikidata_bib](https://lubianat.github.io/wikidata_bib).

# Repository structure
- docs
- notes
    - Q1123.md
    - Q2234.md
- toread.md
- read.ttl
- read.csv

### Explanation

- toread.md

A markdown stack/list of titles of papers. It does not need to be formated, it is mostly a dump of articles that you will want to read.

- read.ttl

An RDF file linking the wikidata URIs for the articles you are reading to your notes. 
Each note file will have an URI. For now I`ll use the property wb:has_notes, where wb is this repository URL

- read.csv 

A csv file linking article titles/human readable info to Wikidata ids.

- notes
A folder containing markdown notes for each article. Each article get its on file, named by Wikidata ID. 
If the material does not fit on Wikidata, just add it as a new header to other.md.

- collections
A series of URIs for the different topics that I am interested in. 

- sparql
Wikidata SPARQL queries for the dashboard on `docs`

- docs
  
The html content for GitHub Pages, providing analytics on what I read. 

## Notes structure

# The title of the work
    The citation in [Manubot](https://manubot.org/) syntax

## A header saying "Highlights"

Copy-and-pasted highlighs from the text. Do not highlight too much and no copy right is infringed. 

--> Any comments made by you should be preceeded by an arrow. And
    if they take another line, it is enough that they are indented.

And then you can continue highlighting

## A header saying "Comments"
Any general comments that did not fit inlinely. 

(now the explanation is over, back to the README we go)

## Features yet to be implemented
- Recording of claims: claims and the papers that support them
- Recording of concepst: concepts and the papers that introduce (or use) them 
- Clean the code that makes the automatic updates

- Auto update queries in GH Pages 
I do not know how to embed the queries in the html directly yet.

I am manually getting the urls from the Wikidata Query Service
using queries in the sparql folder.