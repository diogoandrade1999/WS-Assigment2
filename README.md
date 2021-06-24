# WS-Assigment2

## Dataset URL

-   https://www.kaggle.com/shivamb/netflix-shows

## Create Repository in GraphDB

-   Setup > Repositories > Create new repository > GraphDB Free
    -   Repository ID: shows
    -   Ruleset: RDFS

## Import data in GraphDB

-   Import > RDF > Import RDF files
    -   data/shows.nt
    -   data/showsont.n3
    -   Import

### URL Repository

-   http://127.0.0.1:7200/repositories/shows

## USAGE Conversor csv to nt

```bash
$ python3 conversor/conversor.py -f data/shows.csv
```

## EXECUTE APP

```bash
$ pip3 install -r requirements.txt
$ python3 app/manage.py runserver
```