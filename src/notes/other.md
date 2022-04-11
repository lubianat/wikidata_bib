# Blog posts and web pages

# Azimuth References
https://azimuth.hubmapconsortium.org/references/


Human - PBMC

--> species neutral annotations are relatively ok. Some terms are not covered, e.g. ASDC AXL+ Dendritic Cell is mapped to "dendritic cell" only .

Originally described in Bakken et al, bioRxiv 2020, this data was the integrated across the two individual donors to create the Azimuth reference used here. Annotations are provided at the level of class (e.g. GABAergic), subclass (e.g. L2/3 IT), cluster (e.g. Inh L1-2 VIP WNT4), and cross-species cluster (e.g. Sst_6).

--> Interesting; instead of an ontological organization, multiple annotation files. Cell Ontology annotations are very general.


Mouse - Motor Cortex

Annotations are provided at the level of class (e.g. GABAergic), subclass (e.g. L2/3 IT), cluster (e.g. L2/3 IT_3), and cross-species cluster (e.g. Sst_6)

Non-Neuronal	Non-neuronal cell	animal cell
Chandelier	Chandelier neuron	GABAergic neuron	

--> hm, super general labels

Human - Pancreas

--> CL labels seem good

Human - Fetal Development

--> No CL annotation

Human - Lung

--> Relatively good annotations

Annotation is missing for state+type labels.


# Tagging the Scientific Abstracts with Wikidata Items
https://dwayzer.netlify.app/posts/2021-06-15-tagging-the-abstracts-with-wikidata-items/

Scholia - a brilliant tool, offers  (https://scholia.toolforge.org/text-to-topics>) convertor, which also requires a manual input. Its open code is available at Github, but my R+/P- phenotype leaves me no chance for its adoption.

There is also an R-solution for text search in Wikidata - a new WikidataR package (still in development) offers a “find item” function. It is a wrapper for Wikimedia API module named wbsearchentities that does a very generic search. Try to do query a term “galaxy” and in addition to an astronomical structure, you will have the LA footbal club, military aircraft, US record label, etc, etc.

the authors usually suggest the keywords (not always good ones though), which could be used for initial setting of subject area;

the indexing services (like Medline, Semantics Scholar, Scopus) also assign the terms (not equally well for all subjects though). Some of them provide free API.

 I utilized CrossRef API example to obtain the abstracts of 5 random articles published after Jan 2020.

The package udpipe offers a set of functions for Tokenization, Parts-of-Speech (POS) tagging, Lemmatization, Dependency Parsing, etc.


check against the dictionaries and thesauri (a long chain of wdt:P_ in a code. Some thesauri have direct relations to the scientific concepts (like MeSH - P486, ChEBI ID - P683, Semantic Scholar topic ID - P6611), the others are rather dictionaries and encyclopedias (like Oxford Classical Dictionary - P9106, or Enciclopaedia Britannica - P1417). You should be aware that those terms are also not completely matched to Wikidata items (see Mix’n’Match for particular catallogues).

excludes disambiguation wikimedia pages (Q4167410) - there’s over 1M such pages in Wikidata.

filters only English terms

filters the terms found at least in 3 thesauri

--> Cool method. Will fail for less curated concepts, though. 

 a prototype of checking template - an interactive DT table that:

shows the text excerpts containg the term (+/- 2 words around)

highlights the terms

provides a description of the found Wikidata item

can be edited (right here! Click on ? and change it to “yes” in valid? column)


Limitations
there could be more relevant items for the terms, but I have not found it. Sure. So far this can be viewed as an initial suggestion and a pointer. Each item in the table above directs via URL to a Wikidata page where the related items can further be found.

Another option that I haven’t tried is to check if the items retrieved by initial API request are main subjects, P921 present in any scientific articles, Q13442814 or (more generally) with the items published, P1433 in the academic journals, Q5633421.



# Biolink Model 

https://biolink.github.io/biolink-model/

The schema is expressed as a YAML, which is translated to:

    Individual pages for each class in the model, e.g https://w3id.org/biolink/vocab/Gene
    An OWL ontology, also available on BioPortal
    Python dataclasses, also available on PyPI
    ShEx (RDF shape constraints)
    graphql (Experimental)
    protobuf (Experimental)
    json-schema (Experimental)

Slots are used to collectively refer to, both, node and edge properties.

There are two types of slots defined in the model,

    node property - all node properties are a sub-class of node property
    association slot - all edge properties are a sub-class of association slot

Browse the Biolink Model to explore all defined entities, associations, and slots.

--> It sounds a bit weird, I'd imagine then as instances , not subclasses

You can use Biolink Model as a schema for labelled property graphs (Neo4j) or for edge labelled graphs (RDF).

To that end, Biolink Model makes use of linkML (Biolink Modeling Language) for defining the various semantics of the model.

The modeling language provides the following idioms,

    Class definition
        Used to define classes
    Slot definition
        Used to define class properties
    Type definition
        Used to define data types
    Schema definition
        Used to define properties of the model itself


A class represents an entity or an association

Within the Biolink Model there are two hierarchies of classes:

    Named Things (nodes)
    Associations (edges)

Mixins are classes that contain slots (properties) or slots which embody a generic slot semantic definition, for use across several other classes or slots.

Mixins are abstract classes/slots and they cannot be instantiated by themselves. That is, there cannot be an instance of a mixin class or slot value (e.g. predicate slot) used as ‘data’

Mixins do not contribute to the inheritance hierarchy of the class that uses them.

Slots

In Biolink Model, slots represent properties that a class can have.

A slot is similar to rdf:Property where it can link

    an instance of a class to another instance of a class
    an instance of a class to a literal/data type

In Biolink Model slots are used to represent

    Predicates
    Node Properties
    Edge Properties

n Biolink Model we have several data types.

Data types do not have any inheritance and thus are not arranged in any hierarchy.

For example, iri type is a type defined in the Biolink Model where the value space is constrained to uriorcurie.

Biolink Model has several entity classes like gene, disease, phenotypic feature, chemical substance.

All these classes are arranged in a hierarchy with the root of all entities being the named thing class.

Biolink Model has several Association classes like gene to gene association, gene to disease association, disease to phenotypic feature association.

What are the mapping(s) for this class?

    Mappings are a way of rooting this new association in the context of other ontologies, thesauri, controlled vocabularies and taxonomies
    Determine the level of granularity for your mappings where they can be divided into 5 types: related_mappings, broad_mappings, narrow_mappings close_mappings, exact_mappings


Here we define that the entity class gene is a sub-class of gene or gene product. Note that is_a has the characteristics of homeomorphicity: is_a SHOULD only connect either (1) two mixins (2) two classes (3) two slots.



## WBStack setting changes, Federated properties, Wikidata entity mapping & more
https://addshore.com/2021/05/wbstack-setting-changes-federated-properties-wikidata-entity-mapping-more/

 WBStack as part of an effort to explore the WBaaS (Wikibase as a service) topic during the year, as outlined by the development plan.
Here is a quick rundown of what’s new and improved.

The Wikibase team developed an extension called WikibaseManifest in 2020. This extension is now loaded onto all WBStack sites.

One of the manifest features allows mapping of entities on a local wikibase to wikidata entities.


## Ontologies in Neo4j: Semantics and Knowledge Graphs 
https://neo4j.com/blog/ontologies-in-neo4j-semantics-and-knowledge-graphs/#A-brief-introduction

-->  Ontologies in Neo4j: Semantics and Knowledge Graphs  - 1.2.4. Wikidata and Knowledge Graphs

neosemantics (n10s)

neosemantics is a plugin that enables the use of RDF in Neo4j
https://github.com/neo4j-labs/neosemantics


The first characteristic of an ontology is it has to be a formal representation. It has to be machine readable, that’s a key point. It has to have some structured form.

The second characteristic is the ontology is an explicit description of a domain. It

The third characteristic is the notion of consensuated knowledge, it’s a shared vocabulary. This vocabulary is typically shared by a community.

 First, we have Neo4j as the data store and I’m going to use an extension that I’ve been working on and I’ve actively developed called NeoSemantics.


Some relatively simply on-map graph matching between different databases

The Wikbase team also developed worked on initial steps toward property federation in 2020, and this functionality is not available on WBStack (though the setting comes with a warning).

This initial property federated step allows use of properties from Wikidata directly on your Wikibase site, currently at the cost of having your own properties.

A next iteration of this functionality is on the Wikibase roadmap for 2021.

## What Is an Individual? Biology Seeks Clues in Information Theory.

Even on Earth today, it’s clear that nature has a sloppy disregard for boundaries: Viruses rely on host cells to make copies of themselves. Bacteria share and swap genes, while higher-order species hybridize. Thousands of slime mold amoebas cooperatively assemble into towers to spread their spores. Worker ants and bees can be nonreproductive members of social-colony “superorganisms.” Lichens are symbiotic composites of fungi and algae or cyanobacteria. Even humans contain at least as many bacterial cells as “self” cells, the microbes in our gut inextricably linked with our development, physiology and survival.

“biology as a field is completely under-theorized,” said Manfred Laubichler, a theoretical biologist at Arizona State University. “It’s very much still an empirically driven discipline.”

arbitrary ways that concepts of individuality were applied in the study of natural selection and other biological processes.

Unfortunately, “once gene theory took over, it became a biology of things,” said Scott Gilbert, a developmental biologist at Swarthmore College. But now that’s starting to change again. “Twentieth-century biology was a biology of things,” he said. “Twenty-first-century biology is a biology of processes.”

 the organismal individual, an entity that is shaped by environmental factors but is strongly self-organizing

 The second type of individuality is the colonial form, ant colony or a spiderweb.

 The third type is driven almost entirely by the environment.

 according to Krakauer. “What we’re trying to do is discover a whole zoo of life forms that extend far beyond what we have conventionally called living,” he said.

 And if researchers can gain a better understanding of the factors that have the greatest impact on a system’s individuality, they might learn more about evolutionary transitions like the emergence of multicellularity.

“I think that defining fundamental quantities helps us to suddenly start to see dynamics that we didn’t see before, and understand processes that we hadn’t thought of before,” 

“Organisms aren’t just individuated,” he said. “They have access to information about their individuation.” To him, the kind of information that Krakauer and Flack’s framework uses might not be “knowable” to an organism: “It’s not clear to me that the organism could use these information metrics that they define in a way that would allow it to preserve its existence,” he said.



## (Nano)Publish your research with Python
https://blog.esciencecenter.nl/nano-publish-your-research-with-python-b81aa54eb1a2


1.1.3. Interoperable publication processes: nanopublications


How do we formally communicate such findings such that they may be cited and credit attributed accordingly? One means of achieving this is to use ‘nanopublications’.

Today, we proudly present to you the result of this desire: the nanopub Python library.

--> nice
Assertion: The assertion is the main content of a nanopublication. This is generally some kind of scientific claim (an observation, result, interpretation of someone else’s result etc.)

Provenance: This part describes how the assertion above came to be.

Publication Info: This part contains metadata about the nanopublication as a whole, such as when and by whom it was created.

from nanopub import Publication, NanopubClient
    client = NanopubClient()
    results = client.find_nanopubs_with_text('Picoides')
    for result in results:
        print(result)

Hold on, I want to publish Nanopublications of my own!

To publish to the nanopub server you need to set up your profile. This allows the nanopub server to identify you. Run the following interactive command (on the command line):

setup_nanopub_profile

client.claim('All cats are gray')

Published to http://purl.org/np/RA47eJP2UBJCWuJ324c6Qw0OwtCb8wCrprwSk39am7xck

Or, to leverage the true power of semantic technologies, you can build your own RDF graph of triples and publish that

--> Nice, uses rdflib

nanotate: Create nanopublications from annotations in PDF-files made with hypothes.is

--> hmm, that is _very_ interesting for both 3.2. Community annotation of texts via Wikidata and  3.2.1. Pilot: Annotation of the Human Cell Atlas corpus

 



## Tabula Sapiens
Tabula Sapiens will be a benchmark, first-draft human cell atlas of two million cells from 25 organs of eight normal human subjects.


onsiderable investment was made in generating these data and we ask that you respect rights of first publication and acknowledgment as outlined in the Toronto agreement (Toronto International Data Release Workshop Authors. Prepublication data sharing. Nature. 2009 Sep 10;461(7261):168-70)
--> Interesting


# Dataset (Google Advanced Search Engine Optimization)

 Google's approach to dataset discovery makes use of schema.org and other metadata standards that can be added to pages that describe datasets

 https://toolbox.google.com/datasetsearch/

 Here are some examples of what can qualify as a dataset:
 - Anything that looks like a dataset to you

Add the required properties. For information about where to put structured data on the page, watch JSON-LD structured data: Where to insert on the page.
Follow the guidelines.
Validate your code using the Rich Results Test.
Deploy a few pages that include your structured data and use the URL Inspection tool to test how Google sees the page

Here's an example for datasets using JSON-LD and schema.org syntax.


The full definition of Dataset is available at schema.org/Dataset.

Use unique names for distinct datasets whenever possible.

A tabular dataset is one organized primarily in terms of a grid of rows and columns. For pages that embed tabular datasets, you can also create more explicit markup, building on the basic approach described above. At this time we understand a variation of CSVW ("CSV on the Web", see W3C), provided in parallel to user-oriented tabular content on the HTML page.

Monitor rich results with Search Console

## Understand how structured data works

Google uses structured data that it finds on the web to understand the content of the page, as well as to gather information about the web and the world in general. For example, here is a JSON-LD structured data snippet that might appear on a recipe page, describing the title of the recipe, the author of the recipe, and other details

 Most Search structured data uses schema.org vocabulary, but you should rely on the documentation on developers.google.com as definitive for Google Search behavior


Google Search supports structured data in the following formats, unless documented otherwise:

JSON-LD* (Recommended)	
A JavaScript notation embedded in a <script> tag in the page head or body. 

Microdata	An open-community HTML specification used to nest structured data within HTML content.

RDFa	An HTML5 extension that supports linked data by introducing HTML tag attributes

## Making it easier to discover datasets
https://www.blog.google/products/search/making-it-easier-discover-datasets/

To enable easy access to this data, we launched Dataset Search, so that scientists, data journalists, data geeks, or anyone else can find the data required for their work and their stories, or simply to satisfy their intellectual curiosity.

Similar to how Google Scholar works, Dataset Search lets you find datasets wherever they’re hoste

Our approach is based on an open standard for describing this information (schema.org) and anybody who publishes data can describe their dataset this way. We encourage dataset providers, large and small, to adopt this common standard so that all datasets are part of this robust ecosystem.

A search tool like this one is only as good as the metadata that data publishers are willing to provide. We hope to see many of you use the open standards to describe your data

# GitHub repositories


## HCA metadata schemas ( https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/schema_style_guide.md)

--> Metadata challenges - 1.4. The challenges of the Human Cell Atlas

Introduction

    DISCLAIMER: At this time, the HCA Metadata Standard development team is actively working towards adhering to this style and formatting guide. In some cases, the standard might not yet follow all the guidelines outlined in this document. Your patience is appreciated!

This document describes the style and formatting rules followed by the HCA Metadata Standard for JSON schemas and fields. The goals of the Metadata Standard are to improve the accessibility, (re-)usability, and quality of data submitted to the HCA. In order to develop a high-quality, robust Metadata Standard, we propose the following guidelines and aim to adhere to them as the standard evolves and adapts to changing technologies.



name: A programmatic, unqualified name for the schema. The name is the name of the schema which should be in all lowercase and snake_case. This attribute is used by the DCP software to identify the schema, and the name should match the filename of the schema absent the .json file extension.

type and properties: The type of the schema (should always be object) followed by the metadata fields (properties).

$id: A persistent URI for the schema. The $id attribute is not included in JSON schemas in GitHub. Instead, it is inserted automatically at the time schemas are published to the HCA Metadata Standard at schema.humancellatlas.org.

Example:

 {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "description": "Information about an organoid biomaterial.",
     "additionalProperties": false,
     "required": [
         "describedBy",
         "schema_type",
         "biomaterial_core",
         "model_for_organ"
     ],
     "title": "Organoid",
     "name": "organoid",
     "type": "object",
     "properties": {
         ...
     }
 }



    HCA unqualified field name: diseases

    HCA qualified field name: donor_organism.diseases
    HCA qualified field name: specimen_from_organism.diseases

Qualified field names need to be unique among all schemas

The following attributes are required for each metadata field in an HCA metadata schema.

    description: A clear, concise statement of the what the metadata field is. The description value will appear in the metadata spreadsheet and be displayed in the Metadata Dictionary on the Data Portal.

    type: The JSON type of value required for the metadata field. The type value will be displayed in the Metadata Dictionary on the Data Portal.

    user-friendly: A user-facing, readable term or phrase for the metadata field name. The user-friendly value will appear in the metadata spreadsheet, be displayed in the Data Browser, and be displayed in the Metadata Dictionary on the Data Portal.

Changing a user-friendly value is a patch change to the schema version and is thus easier and simpler to implement than changing a field name (which is a major change to the schema version).

Special case: Ontology examples

Example values can be supplied for fields that are governed by an ontology by including them in the ontology schema. The text, ontology, and ontology_label fields can all take example valid values.

Example:

 module/ontology/species_ontology.json:
 
 "text": {
     "description": "The name of the species to which the organism belongs.",
     "type": "string",
     "example": "Human",
     ...
 },
 "ontology": {
     "description": "An ontology term identifier in the form prefix:accession",
     "type": "string",
     "example": "NCBITaxon:9606",
     ...
 },
 "ontology_label": {
     "description": "The preferred label for the ontology term referred to in the ontology field. This may differ from the user-supplied value in the text field.",
     "type": "string",
     "example": "Homo sapiens",
     ...
 }

Spelling and grammer

    Use American English spelling of words. e.g.: "meter" instead of "metre". This standard is in line with the HCA DCP.
    Use Oxford comma in lists. Exception is when using a semi-colon to separate multiple example values in the example attribute.
    Use present tense

### The Human Cell Atlas: Overview of Metadata Structure
https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/structure.md

There are five major entities supported by the HCA metadata standard: Projects, Biomaterials (biological samples), Protocols, Processes, and Files

The entities are arranged in units that represent different parts of an experiment. For example, the diagram below is an abstract illustration of an input biomaterial (e.g., a tissue sample) undergoing a process (e.g., dissociation) to produce another biomaterial (e.g., a sample of dissociated cells). The process that was executed followed a specific protocol - or intended plan - to produce the output biomaterial.

Some example URIs include:

http://schema.humancellatlas.org/core/biomaterial/5.0.1/biomaterial_core

#### Field name conventions
--> Field name conventions from HCA might be useful for MIANCT - 3.10 Minimal Information Abount New Cell Classes


Field names should be all lowercase and snake_case.

Field names should be plural if their values are arrays.
#### Field description tone and voice

Make a statement instead of a demand. For example:

    Use

        "description": "Age of the donor."
    
    not
    
        "description": "Enter the age of the donor."

Be concise.
1. Use a formal writing voice. Avoid first-person pronouns, using "you", contractions, and slang.
#### Field example conventions

1. Include one or two examples per field, when appropriate . Two examples - separated by a semicolon - should be used when a range of values are valid to illustrate potential breadth of values. A single example should be used otherwise to illustrate general usage of the field. 
2. 
Do not include instructions for entering a value. Instructions should be entered in the "guidelines" attribute. For example: 

    Use
    
        "insdc_study": {
            "guidelines": "Accession must start with PRJE, PRJN, or PRJD.",
            "example": "PRJNA000000",
            ...
        },

### Ontology vs. enum vs. free text

Metadata fields will benefit from using a controlled vocabulary to restrict valid values. Such restrictions enable data consumers to filter, search, or order fields based on values of interest without having to account for different values that mean the same thing. For example, the `genus_species` field benefits from using a controlled vocabulary so that all human data is annotated with `"genus_species": "Homo sapiens"` instead of with other possible values such as "Human" (colloquial term), "homo sapiens" (different case), "Homo sapeins" (misspelling), or "Hs" (shorthand). 

The HCA Metadata Standard is committed to using controlled vocabularies - in the form of externally maintained **ontologies** and JSON **enums** - to standardize valid values for metadata fields. In most cases, using an ontology is preferred over using a JSON *enum* provided that an appropriate ontology with good or full coverage is available. 

Finally, if the list of valid values for a field is very long - for example more than ten valid values - and does not have an appropriate ontology, a free text field is preferred as it means data submitters will not need to constantly validate against the enum (which can be frustrating).


# Websites


## The Human Protein Atlas 

### https://www.proteinatlas.org/about/assays+annotation


The single cell RNA sequencing dataset is based on meta-analysis of literature on single cell RNA sequencing and single cell databases that include healthy human tissue

In total, single cell transcriptomics data for 13 tissues and peripheral blood mononucleated cells (PBMCs) were analyzed. These datasets were respectively retrieved from the Single Cell Expression Atlas, the Human Cell Atlas, the Gene Expression Omnibus, and the European Genome-phenome Archive. The complete list of references is shown in the table below.


Unfiltered data were used as input for downstream analysis with an in-house pipeline using Scanpy (version 1.4.4.post1) in Python 3.7.3

Defining cell types

Each of the 192 different cell type clusters were manually annotated based on an extensive survey of >500 well-known tissue and cell type-specific markers, including both markers from the original publications, and additional markers used in pathology diagnostics. For each cluster, one main cell type was chosen by taking into consideration the expression of different markers. For a few clusters, no main cell type could be selected, and these clusters were not used for classification. The most relevant markers are presented in a heatmap on the Cell Type Atlas, in order to clarify cluster annotation to visitors.

-->           1.4.2.3. Cell label identification
-->          1.4.2.3.1. Labelling clusters

-->   3.1.  Cell-type markers in Wikidata

Cell type dendrogram
The cell type dendrogram presented on the Cell Type Atlas shows the relationship between the single cell types based on genome-wide expression. The dendrogram is based on agglomerative clustering of 1 - Spearman's rho between cell types using Ward's criterion. The dendrogram was then transformed into a hierarchical graph, thus where link distances were normalized to emphasize graph connections rather than link distances. Link width is proportional to the distance from the root, and are colored according to cell type group if only one cell type group is present among connected leaves.

--> "cell type group"


### https://www.proteinatlas.org/humanproteome/celltype

--> Very granular, specific pages for a number of generic cell types, like "neuronal cells." Lots of descriptions and images, super cool resource. 


Classification of all protein-coding genes based on single cell type-specific expression, determining the number of genes elevated (cell type/group enriched, cell type enhanced) in a particular cell type compared to all other cell types.

-> Table containing simple ontology relating each "cell type group"  to many "cell types"





--> Site is super queriable!


### https://www.proteinatlas.org/search/cell_type_category_rna:any;Cell%20type%20enriched%20AND%20sort_by:tissue%20specific%20score

-->   3.1.  Cell-type markers in Wikidata
100%