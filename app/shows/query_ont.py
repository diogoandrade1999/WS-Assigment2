from SPARQLWrapper import SPARQLWrapper, JSON


URL = "http://127.0.0.1:7200/repositories/shows"


def list_celebrity(page):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        prefix pred: <http://shows.org/pred/>

        SELECT DISTINCT ?celname ?popularity (GROUP_CONCAT(?title;SEPARATOR=";") AS ?titles)
        WHERE {
            ?cel a show:People .
            ?cel pred:name ?celname .
            ?cel pred:popularity ?popularity .
            ?cel pred:dualrole ?show .
            ?show pred:title ?title .
        } GROUP bY ?celname ?popularity OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                celebrity = d['celname']['value']
                titles = d['titles']['value']
                popularity = d['popularity']['value']
                if titles != "":
                    titles = titles.split(';')
                else:
                    titles = []
                results[celebrity] = {'titles': titles, 'popularity': popularity}
        return results
    except Exception:
        return {}


def search_celebrity(page, name):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        prefix pred: <http://shows.org/pred/>

        SELECT DISTINCT ?celname ?popularity (GROUP_CONCAT(?title;SEPARATOR=";") AS ?titles)
        WHERE {
            ?cel a show:People .
            ?cel pred:name ?celname .
            ?cel pred:popularity ?popularity .
            ?cel pred:dualrole ?show .
            ?show pred:title ?title .
            FILTER regex(str(?celname), """ + "\"" + name + "\"" + """, "i") .
        } GROUP bY ?celname ?popularity OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                celebrity = d['celname']['value']
                titles = d['titles']['value']
                popularity = d['popularity']['value']
                if titles != "":
                    titles = titles.split(';')
                else:
                    titles = []
                results[celebrity] = {'titles': titles, 'popularity': popularity}
        return results
    except Exception:
        return {}


def list_shows_type():
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        prefix pred: <http://shows.org/pred/>

        SELECT ?typename
        WHERE {
            ?type a show:Type .
            ?type pred:type ?typename .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [d['typename']['value']]
        return results
    except Exception:
        return None


def list_shows_countries():
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        prefix pred: <http://shows.org/pred/>

        SELECT ?countryname
        WHERE {
            ?country a show:Country .
            ?country pred:country ?countryname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [d['countryname']['value']]
        return results
    except Exception:
        return None


def list_shows_listed_in():
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        prefix pred: <http://shows.org/pred/>

        SELECT ?listed_inname
        WHERE {
            ?listed_in a show:ListedIn .
            ?listed_in pred:listed_in ?listed_inname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [d['listed_inname']['value']]
        return results
    except Exception:
        return None
