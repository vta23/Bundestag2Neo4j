from neo4j import GraphDatabase, basic_auth
from xml.dom import minidom
import glob, os
import time
from tqdm import tqdm

#Database Login data

uri = "bolt://localhost"
driver = GraphDatabase.driver(uri, auth=basic_auth("neo4j", "password"))
session = driver.session()


## Generic Functions:

def matchNode(label, attribute, value):
    def matchNode_int(label,attribute,value):
       try:
           return session.run("MATCH (a:"+label+") WHERE a."+attribute+"= $value RETURN id(a)", value=value).single().value()
       except:
           return None
    match = matchNode_int(label,attribute,value)
    if match is None:
        for i in range(5):
            match_int = matchNode_int(label,attribute,value)
            if match_int is not None:
                 match = match_int
    return match


def createNode(label, attribute1, value1, attribute2 = None, value2 = None, attribute3 = None, value3 = None):
    if attribute3:
        session.run("CREATE (a:" + label + " { " + attribute1 + ": $value1, " + attribute2 + ": $value2, " + attribute3 + ": $value3 })", value1=value1, value2=value2, value3=value3)
    else:
        if attribute2:
            session.run(
                "CREATE (a:" + label + " { " + attribute1 + ": $value1, " + attribute2 + ": $value2 })",
                value1=value1, value2=value2)
        else:
            session.run(
                "CREATE (a:" + label + " { " + attribute1 + ": $value1 })",
                value1=value1)
    return None

def addLabel(nodeid, label):
    session.run("MATCH (a) WHERE id(a) = $nodeid SET a:"+label+"", nodeid=nodeid)
    return None

def addAttribute(nodeid, attribute, value):
    session.run("MATCH (a) WHERE id(a) = $nodeid SET a."+attribute+" = "+value+"", nodeid=nodeid)
    return None

def createRelation(nodeid1, nodeid2, reltype, attribute = None, value = None):
    if attribute == None:
        session.run("MATCH (a),(b) WHERE id(a) = $nodeid1 AND id(b) = $nodeid2 CREATE (a)-[r:" + reltype + "]->(b)",
            nodeid1=nodeid1, nodeid2=nodeid2)
    else:
        session.run("MATCH (a),(b) WHERE id(a) = $nodeid1 AND id(b) = $nodeid2 CREATE (a)-[r:"+reltype+" { "+attribute+": "+value+"}]->(b)", nodeid1=nodeid1, nodeid2=nodeid2)
    return None

def getAttribute(nodeid,attribute):
    x = session.run("MATCH (a) WHERE id(a) = $nodeid RETURN (a." + attribute + ")", nodeid=nodeid)
    return x.single()["(a." + attribute + ")"]



## Functions specific to BT-Drucksachen & Database Structure

# Loading Functions:

def loadDrucksache(document):
    mydoc = minidom.parse(document)
    wahlperiode = mydoc.getElementsByTagName('WAHLPERIODE')[0].childNodes[0].data
    dokumentart = mydoc.getElementsByTagName('DOKUMENTART')[0].childNodes[0].data
    drstyp = mydoc.getElementsByTagName('DRS_TYP')[0].childNodes[0].data
    nr = mydoc.getElementsByTagName('NR')[0].childNodes[0].data
    datum = mydoc.getElementsByTagName('DATUM')[0].childNodes[0].data
    titel = mydoc.getElementsByTagName('TITEL')[0].childNodes[0].data
    text = mydoc.getElementsByTagName('TEXT')[0].childNodes[0].data
    quotedtext = '"%s"' % text
    quoteddrstyp = '"%s"' % drstyp

    k_urheber_list = mydoc.getElementsByTagName('K_URHEBER')
    k_urheber = [None] * (len(k_urheber_list))
    for i in range(len(k_urheber_list)):
        k_urheber[i] = k_urheber_list[i].childNodes[0].data

    p_urheber_list = mydoc.getElementsByTagName('P_URHEBER')
    p_urheber = [None] * (len(p_urheber_list))
    for i in range(len(p_urheber_list)):
        p_urheber[i] = p_urheber_list[i].childNodes[0].data

    if matchNode(dokumentart, "nr", nr) == None:
        createNode(dokumentart, "nr", nr, "datum", datum, "titel", titel)
        id_document = matchNode(dokumentart, "nr", nr)
        addAttribute(id_document, "type", quoteddrstyp)
        createNode("dr_text", "nr", nr, "text", quotedtext)
        id_text = matchNode("dr_text", "nr", nr)
        createRelation(id_text,id_document, "BELONGS_TO")

        id_wahlperiode = matchNode("Wahlperiode", "nr", wahlperiode)
        if id_wahlperiode == None:
            createNode("Wahlperiode", "nr", wahlperiode)
            id_wahlperiode = matchNode("Wahlperiode", "nr", wahlperiode)
        createRelation(id_document, id_wahlperiode, "PUBLISHED_IN")

        for i in range(len(k_urheber)):
            id_k_urheber = matchNode("Institution", "name", k_urheber[i])
            if id_k_urheber == None:
                createNode("Institution", "name", k_urheber[i])
                id_k_urheber = matchNode("Institution", "name", k_urheber[i])
            createRelation(id_k_urheber, id_document, "AUTHORED")

        for i in range(len(p_urheber)):
            id_p_urheber = matchNode("Person", "name", p_urheber[i])
            if id_p_urheber == None:
                createNode("Person", "name", p_urheber[i])
                id_p_urheber = matchNode("Person", "name", p_urheber[i])
            createRelation(id_p_urheber, id_document, "AUTHORED")
    else:
        print("Drucksache ", nr, "schon vorhanden.")


def loadDrucksachenFolder(directory, filepattern, subfolders='no', subfolderpattern = None):
    if subfolders is not 'yes':
        files = glob.iglob(directory + '/' + filepattern, recursive=True)
    else:
        files = glob.iglob(directory + '/' + subfolderpattern + '/' + filepattern, recursive=True)
    jobsize = 0
    for file in files:
        jobsize = jobsize + 1

    if subfolders is not 'yes':
        files = glob.iglob(directory + '/' + filepattern, recursive=True)
    else:
        files = glob.iglob(directory + '/' + subfolderpattern + '/' + filepattern, recursive=True)
    for file in tqdm(files, None, jobsize):
        loadDrucksache((file))

# Reading functions:


def getDRtext(DrucksacheNr):
    nodeid = matchNode("dr_text","nr", DrucksacheNr)
    return getAttribute(nodeid, "text")

def getDRtitle(DrucksacheNr):
    nodeid = matchNode("DRUCKSACHE","nr", DrucksacheNr)
    return getAttribute(nodeid, "titel")

def getDRlist(wahlperiode = "all", attribute = "nr"):
    if wahlperiode == "all":
        x = session.run("MATCH (a:DRUCKSACHE) RETURN (a." + attribute + ")")
    else:
        wp = str(wahlperiode)
        x = session.run('MATCH (a:DRUCKSACHE)--(b:Wahlperiode) WHERE (b.nr = "' + wp + '") RETURN (a.' + attribute + ')')
    xlist = [None]
    for record in x:
        xlist.append(record[ "(a.nr)"])
    del xlist[0]
    return xlist
