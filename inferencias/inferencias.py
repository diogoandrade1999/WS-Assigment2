from SPARQLWrapper import SPARQLWrapper, JSON, POST


URL = "http://127.0.0.1:7200/repositories/shows"


def dual_role():
    sparql = SPARQLWrapper(URL + "/statements")
    sparql.setMethod(POST)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        PREFIX pred: <http://shows.org/pred/>

        insert {
            ?person pred:dualrole ?show .
        }
        where {
            ?person a show:People .
            ?show pred:director ?person .
            ?show2 pred:cast ?person .
            FILTER(?show = ?show2)
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        sparql.query()
    except Exception:
        pass


def populary_actor(level, low, high):
    sparql = SPARQLWrapper(URL + "/statements")
    sparql.setMethod(POST)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        PREFIX pred: <http://shows.org/pred/>

        insert {
            ?person pred:popularity """ + "\"" + level + "\"" +  """ .
        }
        where {
            select ?person (count(distinct ?show) as ?numbershows)
            where {
                ?person a show:Actor .
                ?show pred:cast ?person .
            } group by ?person
            HAVING (?numbershows >= """ + low + """ && ?numbershows < """ + high + """)
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        sparql.query()
    except Exception:
        pass


def populary_director(level, low, high):
    sparql = SPARQLWrapper(URL + "/statements")
    sparql.setMethod(POST)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        prefix foaf: <http://xmlns.com/foaf/0.1/>

        prefix show: <http://show.org/show/>
        PREFIX pred: <http://shows.org/pred/>

        insert {
            ?person pred:popularity """ + "\"" + level + "\"" +  """ .
        }
        where {
            select ?person (count(distinct ?show) as ?numbershows) (count(distinct ?dualrole) as ?dualroles)
            where {
                ?person a show:Director .
                ?show pred:director ?person .
                ?person pred:dualrole ?dualrole .
            } group by ?person
            HAVING (?dualroles <= 0 && ?numbershows >= """ + low + """ && ?numbershows < """ + high + """)
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        sparql.query()
    except Exception:
        pass


def main():
    dual_role()

    levels = ["Low", "Medium", "High", "Extreme"]
    lowers_a = ["0", "5", "15", "20"]
    highs_a = ["5", "15", "20", "50"]
    lowers_d = ["0", "1", "3", "5"]
    highs_d = ["1", "3", "5", "50"]
    for i in range(4):
        populary_actor(levels[i], lowers_a[i], highs_a[i])
        populary_director(levels[i], lowers_d[i], highs_d[i])


if __name__ == "__main__":
    main()
