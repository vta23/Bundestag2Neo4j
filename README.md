# Bundestag2Neo4j
Python import tool that allows to import documents from German Parliament into a Neo4j Graph database

This tool can import documents from German Parliament (Drucksachen) into a Neo4j Graph Database for further analysis and visualization. It creates a node for each document, as well as nodes and edges for all institutional and individual authors , as well as election periods . Metadata such as date, title, type and nr are saved as attributes of the document node. The actual body / text of the document is saved in a separate node to minimize load times


For this to work you will need:

1. A working instance of a Neo4j Graph Database (see https://neo4j.com)
2. A Python 3 environment, with the current Neo4j Bolt driver for Python installed (1.7 at the time of writing - see https://neo4j.com/docs/api/python-driver/current/) as well as access to the standard libraries (specifically required are xml.dom, glob, os, time and tqdm)
3. XML Files of German Parliament documents (Drucksachen - see https://www.bundestag.de/service/opendata)

Instructions:

1. adapt database login data in dbutils.py
2. adapt folder path to xml Drucksachen in main.py to point to your xml files
3. run main.py

List of Labels / Node types created:

DRUCKSACHE - document node, includes metadata and edges to authors, etc. 
dr_text - node for document text
Institution - node for institutional authors
Person - node for individual authors
Wahlperiode - node for election periods
