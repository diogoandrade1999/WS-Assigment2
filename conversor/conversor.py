import argparse
import csv

url_predicate = "<http://shows.org/pred/{}>"
url_shows = "<http://shows.org/shows/{}>"
url_type = "<http://shows.org/type/{}>"
url_people = "<http://shows.org/people/{}>"
url_country = "<http://shows.org/country/{}>"
url_release_year = "<http://shows.org/release_year/{}>"
url_duration = "<http://shows.org/duration/{}>"
url_listed = "<http://shows.org/listed_in/{}>"


def read(filename):
    data = []
    predicates = []
    types = []
    peoples = []
    countries = []
    years = []
    durations = []
    listed = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                predicates = row
            else:
                # show
                show = row[0]
                show_url = url_shows.format(show.lower().replace(" ", "_"))

                #type
                type_show = row[1]
                type_show_url = url_type.format(type_show.lower().replace(" ", "_"))
                if type_show not in types:
                    types += [type_show]
                    data += [type_show_url + " " + url_predicate.format(predicates[1])  + " \"" + type_show + "\" ."]
                data += [show_url + " " + url_predicate.format(predicates[1])  + " " + type_show_url + " ."]

                # title
                title = row[2].replace("\"", "'").replace("\n", " ")
                data += [show_url + " " + url_predicate.format(predicates[2])  + " \"" + title + "\" ."]

                # directors
                directors = row[3]
                if directors != "":
                    for director in directors.split(","):
                        if director[0] == " ":
                            director = director[1:]
                        director_url = url_people.format(director.lower().replace(" ", "_").replace("\"", ""))
                        if director not in peoples:
                            peoples += [director]
                            data += [director_url + " " + url_predicate.format("name")  + " \"" + director.replace("\"", "'") + "\" ."]
                        data += [show_url + " " + url_predicate.format(predicates[3])  + " " + director_url + " ."]

                # cast
                cast = row[4]
                if cast != "":
                    for actor in cast.split(","):
                        if actor[0] == " ":
                            actor = actor[1:]
                        actor_url = url_people.format(actor.lower().replace(" ", "_").replace("\"", ""))
                        if actor not in peoples:
                            peoples += [actor]
                            data += [actor_url + " " + url_predicate.format("name")  + " \"" + actor.replace("\"", "'") + "\" ."]
                        data += [show_url + " " + url_predicate.format(predicates[4])  + " " + actor_url + " ."]

                # country
                countries_show = row[5]
                if countries_show != "":
                    for country in countries_show.split(","):
                        if len(country) > 1:
                            if country[0] == " ":
                                country = country[1:]
                            country_url = url_country.format(country.lower().replace(" ", "_"))
                            if country not in countries:
                                countries += [country]
                                data += [country_url + " " + url_predicate.format(predicates[5])  + " \"" + country + "\" ."]
                            data += [show_url + " " + url_predicate.format(predicates[5])  + " " + country_url + " ."]

                # date_added
                date_added = row[6]
                data += [show_url + " " + url_predicate.format(predicates[6])  + " \"" + date_added + "\" ."]

                # release_year
                release_year = row[7]
                year_url = url_release_year.format(release_year.lower().replace(" ", "_"))
                if release_year not in years:
                    years += [release_year]
                    data += [year_url + " " + url_predicate.format(predicates[7])  + " " + release_year + " ."]
                data += [show_url + " " + url_predicate.format(predicates[7])  + " " + year_url + " ."]

                # duration
                duration = row[9]
                duration_url = url_duration.format(duration.lower().replace(" ", "_"))
                if duration not in durations:
                    durations += [duration]
                    data += [duration_url + " " + url_predicate.format(predicates[9])  + " \"" + duration + "\" ."]
                data += [show_url + " " + url_predicate.format(predicates[9])  + " " + duration_url + " ."]

                # listed_in
                listed_in = row[10]
                for l in listed_in.split(","):
                    if l[0] == " ":
                        l = l[1:]
                    l_url = url_listed.format(l.lower().replace(" ", "_"))
                    if l not in listed:
                        listed += [l]
                        data += [l_url + " " + url_predicate.format(predicates[10])  + " \"" + l + "\" ."]
                    data += [show_url + " " + url_predicate.format(predicates[10])  + " " + l_url + " ."]

                # description
                description = row[11].replace("\"", "'").replace("\n", " ")
                data += [show_url + " " + url_predicate.format(predicates[11])  + " \"" + description + "\" ."]
    return data


def write(filename, data):
    filename = filename.replace(".csv", ".nt")
    f = open(filename, "w")
    for d in data:
        f.write(d + "\n")
    f.close()


def main(filename):
    write(filename, read(filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="path_file", required=True, help="Path to file of csv data", type=str)
    args = parser.parse_args()

    main(args.path_file)
