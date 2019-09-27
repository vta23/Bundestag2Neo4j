# Bundestag2Neo4j
Python import tool that allows to import documents from German Parliament into a Neo4j Graph database

This tool can import documents from German Parliament (Drucksachen) into a Neo4j Graph Database for further analysis and visualization. It creates a node for each document (Label DRUCKSACHE), as well as nodes and edges for all institutional and individual authors (Labels "Institution" & "Person"), as well as election periods (Label "Wahlperiode"). Metadata such as date, title, type and nr are saved as attributes of the document node. The actual body / text of the document is saved in a separate node (Label "dr_text")


For this to work you will need:
1. A working instance of a Neo4j Graph Database (see https://neo4j.com)
2. A Python 3 environment, with the current Neo4j Bolt driver for Python installed (1.7 at the time of writing - see https://neo4j.com/docs/api/python-driver/current/)
3. XML Files of German Parliament documents (Drucksachen - see https://www.bundestag.de/service/opendata)

Instructions:
1. adapt database login data in dbutils.py
2. adapt folder path to xml Drucksachen in main.py
3. run main.py
