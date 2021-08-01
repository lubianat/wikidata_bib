# Wikidata Bib Manager v0

This repo is a propotype for bibliography management using Wikidata. 

The overarching goal is to leverage linked open data to navigate your studies and personal notes. 

You can check an example of a query dashboard for readings at [lubianat.github.io/wikidata_bib](https://lubianat.github.io/wikidata_bib).

# Repository structure
- docs
- src
- notes
    - Q1123.md
    - Q2234.md
- toread.md
- read.ttl
- read.csv
- config.yaml
- pop
- wadd
- wlog
- wread
- 
### Scaffolding files

- toread.md

A markdown stack/list of titles of papers.

The papers can be organized by sections, with section headers corresponding to the names in the config.yaml file.
Articles are stored as Wikidata identifiers, to automatically pull the information when actually reading. 

You can, of course, store just the name of the article or other information and eventually locate and update the file with the Wikidata QID. 

- read.ttl

An RDF file linking the wikidata URIs for the articles you are reading to your notes. 
Each note file will have an URI. For now I`ll use the property wb:has_notes, where wb is this repository URL

- read.csv 

A csv file linking article titles/human readable info to Wikidata ids.

- notes
A folder containing markdown notes for each article. Each article get its on file, named by Wikidata ID. 
If the material does not fit on Wikidata, just add it as a new header to other.md.

- docs
  
The html content for GitHub Pages, providing analytics on what has been read. 

- config.yaml

A configuration file mapping shortcuts to use in the command line to categories in the toread.md.

### Scripts for use

- wadd

Adds a set of new articles to one of the lists in toread.md. Example for single-cell transcriptomics articles in either Nature or Science: https://w.wiki/3LhF
`$ ./wadd https://w.wiki/3MDs -p --new`

- wlog
Adds a commit to git for the articler read and pushes it to GitHub.
`$ ./wlog`

- wread
Read an article that is not on the list in toread.md. 

`$ ./wread Q107542983`

- pop

Pops the first QID in one of the lists in the toread.md file. The command is followed by a shortcut, specifying which list to look for (this is set up in the config.yaml file). 

For example, `$ ./pop ct` will remove the first QID from the "Cell Types" list and open the article for note-taking.

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