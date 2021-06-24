from SPARQLWrapper import SPARQLWrapper, JSON, POST

URL = "http://127.0.0.1:7200/repositories/shows"


def count_shows():
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT (COUNT(?title) AS ?nshows)
        WHERE {
            ?show pred:title ?title .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            results = int(results['results']['bindings'][0]['nshows']['value'])
        return results
    except Exception:
        return 0


def list_shows(page):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?release_yearname (GROUP_CONCAT(?countryname;SEPARATOR=",") AS ?countriesname) (GROUP_CONCAT(?listed_inname;SEPARATOR=",") AS ?listedname) 
        WHERE {
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:country ?country .
            ?country pred:country ?countryname .
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
            ?show pred:release_year ?release_year .
            ?release_year pred:release_year ?release_yearname .
        } GROUP BY ?title ?typename ?release_yearname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                title = d['title']['value']
                results[title] = {'type': d['typename']['value'],
                                  'countries': list(set(d['countriesname']['value'].split(','))),
                                  'listed_in': list(set(d['listedname']['value'].split(','))),
                                  'release_year': d['release_yearname']['value'],
                                  }
        return results
    except Exception:
        return None


def list_shows_type():
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?typename
        WHERE {
            ?show pred:type ?type .
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
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?countryname
        WHERE {
            ?show pred:country ?country .
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
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?listed_inname
        WHERE {
            ?show pred:listed_in ?listed_in .
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


def list_directors(page):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        PREFIX pred: <http://shows.org/pred/>

        SELECT ?directorname (GROUP_CONCAT(?title;SEPARATOR=";") AS ?titles)
        WHERE {
            ?director a foaf:Person .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            ?show pred:title ?title .
        } GROUP bY ?directorname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                director = d['directorname']['value']
                titles = d['titles']['value']
                if titles != "":
                    titles = titles.split(';')
                else:
                    titles = []
                results[director] = titles
        return results
    except Exception:
        return None


def list_actors(page):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        PREFIX pred: <http://shows.org/pred/>

        SELECT ?actorname (GROUP_CONCAT(?title;SEPARATOR=";") AS ?titles)
        WHERE {
            ?actor a foaf:Person .
            ?show pred:cast ?actor .
            ?actor pred:name ?actorname .
            ?show pred:title ?title .
        } GROUP bY ?actorname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                actor = d['actorname']['value']
                titles = d['titles']['value']
                if titles != "":
                    titles = titles.split(';')
                else:
                    titles = []
                results[actor] = titles
        return results
    except Exception:
        return None


def person_detail(name):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename
            (GROUP_CONCAT(DISTINCT ?directorname;SEPARATOR=";") AS ?directorsname)
            (GROUP_CONCAT(DISTINCT ?countryname;SEPARATOR=";") AS ?countriesname)
        WHERE {
            ?person pred:name """ + "\"" + name + "\"" + """ .
            OPTIONAL {
                ?show pred:director ?person .
                ?show pred:director ?director .
                ?director pred:name ?directorname .
                ?show pred:title ?title .
                ?show pred:type ?type .
                ?type pred:type ?typename .
                ?show pred:country ?country .
                ?country pred:country ?countryname .
            }
        } GROUP BY ?title ?typename
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results1 = {}
            for d in data:
                if 'title' in d:
                    title = d['title']['value']
                    directors = d['directorsname']['value']
                    if directors != "":
                        directors = directors.split(';')
                        directors.remove(name)
                    results1[title] = {'type': d['typename']['value'],
                                       'countries': d['countriesname']['value'].split(';'),
                                       'directors': directors
                                       }
    except Exception:
        results1 = None

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename
            (GROUP_CONCAT(DISTINCT ?actorname;SEPARATOR=";") AS ?castname)
            (GROUP_CONCAT(DISTINCT ?countryname;SEPARATOR=";") AS ?countriesname)
        WHERE {
            ?person pred:name """ + "\"" + name + "\"" + """ .
            OPTIONAL {
                ?show pred:cast ?person .
                ?show pred:cast ?actor .
                ?actor pred:name ?actorname .
                ?show pred:title ?title .
                ?show pred:type ?type .
                ?type pred:type ?typename .
                ?show pred:country ?country .
                ?country pred:country ?countryname .
            }
        } GROUP BY ?title ?typename
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results2 = {}
            for d in data:
                if 'title' in d:
                    title = d['title']['value']
                    cast = d['castname']['value']
                    if cast != "":
                        cast = cast.split(';')
                        cast.remove(name)
                    results2[title] = {'type': d['typename']['value'],
                                       'countries': d['countriesname']['value'].split(';'),
                                       'cast': cast
                                       }
    except Exception:
        results2 = None
    return results1, results2


def show_detail(title):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?typename ?description ?date_added ?release_yearname ?durationname
            (GROUP_CONCAT(DISTINCT ?countryname;SEPARATOR=";") AS ?countriesname)
            (GROUP_CONCAT(DISTINCT ?listed_inname;SEPARATOR=";") AS ?listedname)
            (GROUP_CONCAT(DISTINCT ?directorname;SEPARATOR=";") AS ?directorsname)
            (GROUP_CONCAT(DISTINCT ?actorname;SEPARATOR=";") AS ?castname)
        WHERE {
            ?show pred:title """ + "\"" + title + "\"" + """ .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:country ?country .
            ?country pred:country ?countryname .
            ?show pred:description ?description .
            ?show pred:date_added ?date_added .
            ?show pred:release_year ?release_year .
            ?release_year pred:release_year ?release_yearname .
            ?show pred:duration ?duration .
            ?duration pred:duration ?durationname .
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
            OPTIONAL {
                ?show pred:director ?director .
                ?director pred:name ?directorname .
            }
            OPTIONAL {
                ?show pred:cast ?actor .
                ?actor pred:name ?actorname .
            }
        } GROUP BY ?typename ?description ?date_added ?release_yearname ?durationname
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            for d in data:
                directors = d['directorsname']['value']
                if directors != "":
                    directors = directors.split(';')
                cast = d['castname']['value']
                if cast != "":
                    cast = cast.split(';')
                results = {'type': d['typename']['value'],
                           'description': d['description']['value'],
                           'date_added': d['date_added']['value'],
                           'release_year': d['release_yearname']['value'],
                           'duration': d['durationname']['value'],
                           'countries': d['countriesname']['value'].split(';'),
                           'listed_in': d['listedname']['value'].split(';'),
                           'directors': directors,
                           'cast': cast
                           }
        return results
    except Exception:
        return None


def search_shows(page, title, types_list, countries_list, listed_in_list):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?release_yearname (GROUP_CONCAT(?countryname;SEPARATOR=",") AS ?countriesname) (GROUP_CONCAT(?listed_inname;SEPARATOR=",") AS ?listedname) 
        WHERE {
            ?show pred:title ?title .
            FILTER regex(str(?title), """ + "\"" + title + "\"" + """, "i") .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            FILTER (?typename in (""" + '"' + '\", \"'.join(types_list) + '"' + """))
            ?show pred:country ?country .
            ?country pred:country ?countryname .
            FILTER (?countryname in (""" + '"' + '\", \"'.join(countries_list) + '"' + """))
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
            FILTER (?listed_inname in (""" + '"' + '\", \"'.join(listed_in_list) + '"' + """))
            ?show pred:release_year ?release_year .
            ?release_year pred:release_year ?release_yearname .
        } GROUP BY ?title ?typename ?release_yearname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                title = d['title']['value']
                results[title] = {'type': d['typename']['value'],
                                  'countries': list(set(d['countriesname']['value'].split(','))),
                                  'listed_in': list(set(d['listedname']['value'].split(','))),
                                  'release_year': d['release_yearname']['value'],
                                  }
        return results
    except Exception as e:
        return None


def search_directors(page, name):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?directorname (GROUP_CONCAT(?title;SEPARATOR=";") AS ?titles)

        WHERE {
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            FILTER regex(str(?directorname), """ + "\"" + name + "\"" + """, "i") .
            ?show pred:title ?title .
        } GROUP bY ?directorname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                director = d['directorname']['value']
                titles = d['titles']['value']
                if titles != "":
                    titles = titles.split(';')
                else:
                    titles = []
                results[director] = titles
        return results
    except Exception:
        return None


def search_actors(page, name):
    sparql = SPARQLWrapper(URL)
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?actorname (GROUP_CONCAT(?title;SEPARATOR=";") AS ?titles)
        WHERE {
            ?show pred:cast ?actor .
            ?actor pred:name ?actorname .
            FILTER regex(str(?actorname), """ + "\"" + name + "\"" + """, "i") .
            ?show pred:title ?title .
        } GROUP bY ?actorname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                actor = d['actorname']['value']
                titles = d['titles']['value']
                if titles != "":
                    titles = titles.split(';')
                else:
                    titles = []
                results[actor] = titles
        return results
    except Exception:
        return None


def show_edit(title, description, type_show, countries_list,
              listed_in_list, new_description, new_type_show,
              new_countries_list, new_listed_in_list):
    sparql = SPARQLWrapper(URL + "/statements")
    sparql.setMethod(POST)

    if description != new_description:
        sparql.setQuery("""
            PREFIX pred: <http://shows.org/pred/>

            DELETE {
                ?show pred:description ?description .
            }
            INSERT {
                ?show pred:description """ + "\"" + new_description + "\"" + """ .
            }
            WHERE {
                ?show pred:title """ + "\"" + title + "\"" + """ .
                ?show pred:description ?description .
            }
        """)

        try:
            results = sparql.query()
        except Exception:
            pass

    if type_show != new_type_show:
        sparql.setQuery("""
            PREFIX pred: <http://shows.org/pred/>

            DELETE {
                ?show pred:type ?type .
            }
            INSERT {
                ?show pred:type ?newtype .
            }
            WHERE {
                ?show pred:title """ + "\"" + title + "\"" + """ .
                ?show pred:type ?type .
                ?newtype pred:type """ + "\"" + new_type_show + "\"" + """ .
            }
        """)

        try:
            results = sparql.query()
        except Exception:
            pass

    if countries_list != new_countries_list:
        countries_get = ""
        countries_delete = ""
        countries_insert = ""
        for i, country in enumerate(countries_list):
            if country not in new_countries_list:
                countries_get += "?country" + str(i) + " pred:country " + "\"" + country + "\" .\n"
                countries_delete += "?show pred:country ?country" + str(i) + " .\n"
        for i, country in enumerate(new_countries_list, start=len(countries_list)):
            if country not in countries_list:
                countries_get += "?country" + str(i) + " pred:country " + "\"" + country + "\" .\n"
                countries_insert += "?show pred:country ?country" + str(i) + " .\n"
        sparql.setQuery("""
            PREFIX pred: <http://shows.org/pred/>

            DELETE {
                """ + countries_delete + """
            }
            INSERT {
                """ + countries_insert + """
            }
            WHERE {
                ?show pred:title """ + "\"" + title + "\"" + """ .
                """ + countries_get + """
            }
        """)

        try:
            results = sparql.query()
        except Exception:
            pass

    if listed_in_list != new_listed_in_list:
        listed_in_get = ""
        listed_in_delete = ""
        listed_in_insert = ""
        for i, listed_in in enumerate(listed_in_list):
            if listed_in not in new_listed_in_list:
                listed_in_get += "?listed_in" + str(i) + " pred:listed_in " + "\"" + listed_in + "\" .\n"
                listed_in_delete += "?show pred:listed_in ?listed_in" + str(i) + " .\n"
        for i, listed_in in enumerate(new_listed_in_list, start=len(listed_in_list)):
            if listed_in not in listed_in_list:
                listed_in_get += "?listed_in" + str(i) + " pred:listed_in " + "\"" + listed_in + "\" .\n"
                listed_in_insert += "?show pred:listed_in ?listed_in" + str(i) + " .\n"
        sparql.setQuery("""
            PREFIX pred: <http://shows.org/pred/>

            DELETE {
                """ + listed_in_delete + """
            }
            INSERT {
                """ + listed_in_insert + """
            }
            WHERE {
                ?show pred:title """ + "\"" + title + "\"" + """ .
                """ + listed_in_get + """
            }
        """)

        try:
            results = sparql.query()
        except Exception:
            pass
