from SPARQLWrapper import SPARQLWrapper, JSON, POST

URL = "http://127.0.0.1:7200/repositories/shows"


def list_celebrity(page):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix pred: <http://shows.org/pred/>

        SELECT DISTINCT ?celname
        WHERE {
            ?cel a foaf:Person .
            ?cel pred:name ?celname .
        } GROUP bY ?celname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                celebrity = d['celname']['value']
                results += [celebrity]
        return results
    except Exception:
        return None


def search_celebrity(page, name):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix pred: <http://shows.org/pred/>

        SELECT DISTINCT ?celname
        WHERE {
            ?cel a foaf:Person .
            ?cel pred:name ?celname .
            FILTER regex(str(?celname), """ + "\"" + name + "\"" + """, "i") .
        } GROUP bY ?celname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                celebrity = d['celname']['value']
                results += [celebrity]
        return results
    except Exception:
        return None
