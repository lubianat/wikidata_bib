# Wikidata Bib Manager v0

This repo is a propotype for bibliography management using Wikidata. 

The overarching goal is to leverage linked open data to navigate your studies and personal notes. 

For this prototype, I`ll select some of the papers from the list of "[The top 100 papers:
Nature explores the most-cited research of all time](https://www.nature.com/news/the-top-100-papers-1.16224)" list from 2014 and take notes on them. 

## Repository structure

- toread.md

A markdown stack/list of titles of papers. It does not need to be formated, it is mostly a dump of articles that you will want to read.


- read.ttl

An RDF file linking the wikidata URIs for the articles you are reading to your notes. 

Each note file will have an URI. For now, the github URL will suffice. 

I am not sure which property to use for linking. for now I`ll use wb:has_notes, where wb is this repository URL


