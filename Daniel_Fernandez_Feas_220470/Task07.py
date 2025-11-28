# -*- coding: utf-8 -*-
"""
Task 07 – Querying RDF(s)
Assignment 4 – Linked Data (FI UPM)
""" 

# Descargar validador
import urllib.request
url = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py"
urllib.request.urlretrieve(url, "validation.py")

from validation import Report

# Cargar grafo y namespaces
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

g = Graph()
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials"
g.namespace_manager.bind("ns", Namespace("http://somewhere#"), override=False)
g.parse(github_storage + "/rdf/data06.ttl", format="turtle")

report = Report()

# TASK 7.1a – RDFLib: (clase, superclase)


result = []
for cls in set(g.subjects(RDF.type, RDFS.Class)):
    superclass = g.value(subject=cls, predicate=RDFS.subClassOf)
    result.append((cls, superclass))

report.validate_07_1a(result)

# 
# TASK 7.1b – SPARQL: misma estructura
# 

query_7_1b = """
    SELECT DISTINCT ?c ?sc WHERE {
        ?c a rdfs:Class .
        OPTIONAL { ?c rdfs:subClassOf ?sc . }
    }
"""
report.validate_07_1b(query_7_1b, g)

# 
# TASK 7.2a – Individuos de Person (RDFLib)


ns_people = Namespace("http://oeg.fi.upm.es/def/people#")

classes = {ns_people.Person} | set(
    g.transitive_subjects(RDFS.subClassOf, ns_people.Person)
)

individuals = sorted(
    {ind for c in classes for ind in g.subjects(RDF.type, c)},
    key=str
)

report.validate_07_02a(individuals)

# 
# TASK 7.2b – Individuos de Person (SPARQL)
# 

query_7_2b = prepareQuery("""
    SELECT ?ind WHERE {
        ?ind rdf:type ?c .
        ?c rdfs:subClassOf* ns:Person .
    }
""", initNs={"ns": ns_people, "rdf": RDF, "rdfs": RDFS})

report.validate_07_02b(g, query_7_2b)

# 
# TASK 7.3 – Nombre + tipo de quienes conocen a Rocky

query_7_3 = prepareQuery("""
    SELECT ?name ?type WHERE {
        ?x ns:knows ns:Rocky .
        ?x rdf:type ?type .
        ?x rdfs:label ?name .
    }
""", initNs={"ns": ns_people, "rdf": RDF, "rdfs": RDFS})

report.validate_07_03(g, query_7_3)

# 
# TASK 7.4 – Entidades con colega o colega-de-colega
# ==========================================================

query_7_4 = prepareQuery("""
    SELECT DISTINCT ?name WHERE {
        {
            ?x rdfs:label ?name .
            ?x ns:hasColleague ?y .
        }
        UNION
        {
            ?x rdfs:label ?name .
            ?x ns:hasColleague ?y .
            ?y ns:hasColleague ?z .
        }
    }
""", initNs={"ns": ns_people, "rdfs": RDFS})

report.validate_07_04(g, query_7_4)

# Guardar reporte
report.save_report("_Task_07")

