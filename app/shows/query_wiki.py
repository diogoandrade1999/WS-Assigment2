from SPARQLWrapper import SPARQLWrapper, JSON, POST, SPARQLWrapper2


# https://query.wikidata.org/
def wiki_person_data(name):
    n = '"' + name + '"'
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?item ?itemLabel ?sex_name ?birthLocal_name ?birthDate ?dateOfDeath (group_concat(?profession_name; separator="|") as ?profession_names) WHERE 
    {
    # search for person
    ?item wdt:P31 wd:Q5.
    ?item ?label""" + n + """ @en.
    ?item rdfs:label ?itemLabel.
  
    # search profession and profession name
    ?item wdt:P106 ?profession. 
    ?profession ?label ?profession_name. 
    filter(lang(?profession_name) = 'en').
      
    # sex
    OPtional {?item wdt:P21 ?sex. ?sex ?label ?sex_name. filter(lang(?sex_name) = 'en').}
      
    # country where he/she was born
    OPtional {?item wdt:P27 ?birthLocal. ?birthLocal ?label ?birthLocal_name. filter(lang(?birthLocal_name) = 'en').}
      
    # date of birth
    OPtional {?item wdt:P569 ?birthDate. }
      
    # date of death
    Optional {?item wdt:P570 ?dateOfDeath.}
      
    #FILTER (?profession IN (wd:Q33999) wd:Q2526255, wd:Q28389))          # filter for actors, directors or screenwriters (exclude all other professions)
    FILTER(LANGMATCHES(LANG(?itemLabel),  'en')).                         # english only
    FILTER regex (?itemLabel, "^""" + name + """$").                      # Exact match
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }    # Label in english only
    }
    group by ?item ?itemLabel ?sex_name ?birthLocal_name ?birthDate ?dateOfDeath
    Limit 1
     """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results and results['results']['bindings'] != []:
            data = results['results']['bindings']
            results = {}
            # print(data)
            for d in data:
                results['wiki_link'] = d['item']['value'] if 'item' in d else ""
                results['name'] = d['itemLabel']['value'] if 'itemLabel' in d else ""
                results['sex'] = d['sex_name']['value'] if 'sex_name' in d else ""
                results['birthLocation'] = d['birthLocal_name']['value'] if 'birthLocal_name' in d else ""
                results['birhtDate'] = d['birthDate']['value'] if 'birthDate' in d else ""
                results['deathDate'] = d['dateOfDeath']['value'] if 'dateOfDeath' in d else "still alive"
                results['professions'] = d['profession_names']['value'].split('|') if 'profession_names' in d else ""
            #print(results)
            return results
        else:
            print("Failed to find data")
    except Exception:
        print("Error")
        return None
    return {}


def wiki_show_data(name):
    n = '"' + name + '"'
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?item ?itemLabel ?type_name ?publicatioDate ?time (group_concat(?genre_name; separator="|") as ?genres) (group_concat(?award_name; separator="|") as ?awards)WHERE 
    {
    # search for person
    ?item ?label""" + n + """ @en.
    ?item rdfs:label ?itemLabel.
    FILTER(LANGMATCHES(LANG(?itemLabel),  'en')).
    
    # Type 
    Optional {?item wdt:P31 ?type. ?type rdfs:label ?type_name. FILTER(LANGMATCHES(LANG(?type_name),  'en')).}
      
    # genres
     ?item wdt:P136 ?genre.
     ?genre ?label ?genre_name.
     filter(lang(?genre_name) = 'en').
      
    #publication date
    Optional {?item wdt:P577 ?publicatioDate.}
      
    #duration
    Optional {?item wdt:P2047 ?time.}
      
    # awards
    Optional {?item wdt:P166 ?award. ?award ?label ?award_name. filter(lang(?award_name) = 'en').}
    
    FILTER(LANGMATCHES(LANG(?itemLabel),  'en')).                         # english only
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }    # Label in english only
    }
  group by ?item ?itemLabel ?type_name ?publicatioDate ?time
  Limit 1
  """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results and results['results']['bindings'] != []:
            data = results['results']['bindings']
            results = {}
            # print(data)
            for d in data:
                results['wiki_link'] = d['item']['value'] if 'item' in d else ""
                results['name'] = d['itemLabel']['value'] if 'itemLabel' in d else ""
                results['show_type'] = d['type_name']['value'] if 'type_name' in d else ""
                results['publicatioDate'] = d['publicatioDate']['value'] if 'publicatioDate' in d else ""
                results['duration'] = d['time']['value'] if 'time' in d else ""
                results['genres'] = set(d['genres']['value'].split('|')) if 'genres' in d else []
                results['awards'] = set(d['awards']['value'].split('|')) if 'awards' in d else []
            #print(results)
            return results
        else:
            print("Failed to find data")
    except Exception:
        print("Error")
        return None

    return {}


def dbpedia_search_person(name):
    n = '"' + name + '"'
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(
        """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix ont: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?item ?itemLabel?abstract WHERE { 
     # search person
    ?item a ont:Person.
    ?item ?label """ + n + """@en.
    ?item rdfs:label ?itemLabel.
    FILTER(LANGMATCHES(LANG(?itemLabel),  'en')).

    FILTER regex (?itemLabel, """ + n + """).        # exact name
    Optional {?item ont:abstract ?abstract. FILTER(LANGMATCHES(LANG(?abstract),  'en')).}
    } 
    LIMIT 1
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results and results['results']['bindings'] != []:
            data = results['results']['bindings']
            results = {}
            # print(data)
            for d in data:
                results['db_link'] = d['item']['value'] if 'item' in d else ""
                results['name'] = d['itemLabel']['value'] if 'itemLabel' in d else ""
                results['abstract'] = d['abstract']['value'] if 'abstract' in d else ""
            #print(results)
            return results
        else:
            print("Failed to find data")
    except Exception:
        print("Error")
        return None

    return {}


def db_search_show(name):
    n = '"' + name + '"'
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix ont: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT * WHERE {
     # search can either be a film or a tvShow so we search for both
    Optional {?item a ont:Film. ?item ?label """ + n + """@en. ?item rdfs:label ?itemLabel. FILTER(LANGMATCHES(LANG(?itemLabel),  'en')).}
    Optional {?item a ont:TelevisionShow. ?item ?label """ + n + """@en. ?item rdfs:label ?itemLabel. FILTER(LANGMATCHES(LANG(?itemLabel),  'en')).}

   #
    #FILTER regex (str(?itemLabel) , "Chris Pratt").        # exact name
    Optional {?item ont:abstract ?abstract. FILTER(LANGMATCHES(LANG(?abstract),  'en')).}

    } 
    Limit 1
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results and results['results']['bindings'] != []:
            data = results['results']['bindings']
            results = {}
            # print(data)
            for d in data:
                results['db_link'] = d['item']['value'] if 'item' in d else ""
                results['name'] = d['itemLabel']['value'] if 'itemLabel' in d else ""
                results['abstract'] = d['abstract']['value'] if 'abstract' in d else ""
            #print(results)
            return results
        else:
            print("Failed to find data")
    except Exception:
        print("Error")
        return None

    return {}

