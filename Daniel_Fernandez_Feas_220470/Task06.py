# -*- coding: utf-8 -*-
"""
Task 06 – Modifying RDF(s)
Assignment 4 – Linked Data (FI UPM)
"""

# Descargar validador
import urllib.request
url = 'https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py'
urllib.request.urlretrieve(url, 'validation.py')

from validation import Report

# Imports RDFlib
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS

# Crear grafo y namespaces
g = Graph()
r = Report()

ontology = Namespace("http://oeg.fi.upm.es/def/people#")
person_ns = Namespace("http://oeg.fi.upm.es/resource/person/")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
FOAF  = Namespace("http://xmlns.com/foaf/0.1/")

g.namespace_manager.bind("ontology", ontology)
g.namespace_manager.bind("person", person_ns)
g.namespace_manager.bind("vcard", VCARD)
g.namespace_manager.bind("foaf", FOAF)

# TASK 6.1 — Taxonomía de clases
Person = ontology.Person
Professor = ontology.Professor
AssociateProfessor = ontology.AssociateProfessor
InterimAssociateProfessor = ontology.InterimAssociateProfessor
FullProfessor = ontology.FullProfessor

classes = [
    Person,
    Professor,
    AssociateProfessor,
    InterimAssociateProfessor,
    FullProfessor
]

for cls in classes:
    g.add((cls, RDF.type, RDFS.Class))
    g.add((cls, RDFS.label, Literal(cls.split("#")[-1], datatype=XSD.string)))

g.add((Professor, RDFS.subClassOf, Person))
g.add((AssociateProfessor, RDFS.subClassOf, Professor))
g.add((InterimAssociateProfessor, RDFS.subClassOf, AssociateProfessor))
g.add((FullProfessor, RDFS.subClassOf, Professor))

r.validate_task_06_01(g)

# 
# TASK 6.2 — Propiedades


hasColleague = ontology.hasColleague
hasName = ontology.hasName
hasHomePage = ontology.hasHomePage

# hasColleague
g.add((hasColleague, RDF.type, RDF.Property))
g.add((hasColleague, RDFS.domain, Person))
g.add((hasColleague, RDFS.range, Person))
g.add((hasColleague, RDFS.label, Literal("hasColleague", datatype=XSD.string)))

# hasName
g.add((hasName, RDF.type, RDF.Property))
g.add((hasName, RDFS.domain, Person))
g.add((hasName, RDFS.range, RDFS.Literal))
g.add((hasName, RDFS.label, Literal("hasName", datatype=XSD.string)))

# hasHomePage
g.add((hasHomePage, RDF.type, RDF.Property))
g.add((hasHomePage, RDFS.domain, FullProfessor))
g.add((hasHomePage, RDFS.range, RDFS.Literal))
g.add((hasHomePage, RDFS.label, Literal("hasHomePage", datatype=XSD.string)))

r.validate_task_06_02(g)

# TASK 6.3 — Individuos

Oscar = Namespace("http://oeg.fi.upm.es/resource/person/")["Oscar"]
Asun  = Namespace("http://oeg.fi.upm.es/resource/person/")["Asun"]
Raul  = Namespace("http://oeg.fi.upm.es/resource/person/")["Raul"]

# Oscar
g.add((Oscar, RDF.type, Professor))
g.add((Oscar, RDFS.label, Literal("Oscar", datatype=XSD.string)))
g.add((Oscar, hasName, Literal("Óscar Corcho García", datatype=XSD.string)))
g.add((Oscar, hasColleague, Asun))

# Asun
g.add((Asun, RDF.type, AssociateProfessor))
g.add((Asun, RDFS.label, Literal("Asun", datatype=XSD.string)))
g.add((Asun, hasHomePage, Literal("http://oeg.fi.upm.es/", datatype=XSD.string)))
g.add((Asun, hasColleague, Raul))

# Raul
g.add((Raul, RDF.type, InterimAssociateProfessor))
g.add((Raul, RDFS.label, Literal("Raul", datatype=XSD.string)))
g.add((Raul, hasColleague, Oscar))

r.validate_task_06_03(g)

# TASK 6.4 — VCARD y FOAF para Oscar

g.add((Oscar, VCARD.Given, Literal("Oscar", datatype=XSD.string)))
g.add((Oscar, VCARD.Family, Literal("Corcho", datatype=XSD.string)))
g.add((Oscar, FOAF.email, Literal("oscar@upm.es", datatype=XSD.string)))

r.validate_task_06_04(g)

# Guardar reporte
r.save_report("_Task_06")

