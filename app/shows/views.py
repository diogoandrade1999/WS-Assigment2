from django.shortcuts import render, redirect
from shows.query import *


def home(request):
    return render(request, 'pages/home.html')


def shows(request):
    if request.method == 'GET' or request.method == 'POST':
        params = {'types': list_shows_type(),
                  'countries': sorted(list_shows_countries()),
                  'listed_in': sorted(list_shows_listed_in()),
                  'title': request.GET.get('searchShowTitle'),
                  't_checked': request.GET.getlist('searchShowType'),
                  'c_checked': request.GET.getlist('searchShowCountry'),
                  'l_checked': request.GET.getlist('searchShowListedIn'),
                  }
        if request.method == 'GET':
            page = request.GET.get('page')
            if page == None or \
               (params['title'] is None and \
               params['t_checked'] == params['types'] and \
               params['c_checked'] == params['countries'] and \
               params['l_checked'] == params['listed_in']):
                if page == None:
                    page = 0
                params['title'] = ""
                params['t_checked'] = params['types']
                params['c_checked'] = params['countries']
                params['l_checked'] = params['listed_in']
                params['shows'] = list_shows(int(page))
            else:
                params['shows'] = search_shows(int(page), params['title'], params['t_checked'], params['c_checked'], params['l_checked'])  
        elif request.method == 'POST':
            page = request.POST.get('page')
            page = 0
            params['title'] = request.POST.get('searchShowTitle')
            params['t_checked'] = request.POST.getlist('searchShowType')
            params['c_checked'] = request.POST.getlist('searchShowCountry')
            params['l_checked'] = request.POST.getlist('searchShowListedIn')
            params['shows'] = search_shows(int(page), params['title'], params['t_checked'], params['c_checked'], params['l_checked'])
        page = int(page)
        params['previous_page'] = page - 1 if page > 0 else None
        params['next_page'] = page + 1 if len(params['shows']) == 30 else None
        return render(request, 'pages/shows.html', params)
    return redirect(home)


def show(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        if title == None:
            return redirect(shows)
        params = {'title': title, 'show': show_detail(title)}
        return render(request, 'pages/show.html', params)
    return redirect(shows)


def edit_show(request):
    if request.method == 'GET' or request.method == 'POST':
        title = request.GET.get('title')
        if title == None:
            return redirect(shows)
        params = {'types': list_shows_type(),
                  'countries': sorted(list_shows_countries()),
                  'listed_in': sorted(list_shows_listed_in()),
                  'title': title,
                  'show': show_detail(title),
                  }
        if request.method == 'GET':
            return render(request, 'pages/edit_show.html', params)
        elif request.method == 'POST':
            description = request.POST.get('editShowDescription')
            t_checked = request.POST.get('editShowType')
            c_checked = request.POST.getlist('editShowCountry')
            l_checked = request.POST.getlist('editShowListedIn')
            show_edit(title,
                      params['show'].get('description'),
                      params['show'].get('type'),
                      params['show'].get('countries'),
                      params['show'].get('listed_in'),
                      description,
                      t_checked,
                      c_checked,
                      l_checked)
            return redirect('/show/?title=' + title)
    return redirect(shows)


def directors(request):
    if request.method == 'GET' or request.method == 'POST':
        params = {'name': request.GET.get('searchDirectorName')}
        if request.method == 'GET':
            page = request.GET.get('page')
            if page == None or params['name'] is None:
                if page == None:
                    page = 0
                params['name'] = ""
                params['directors'] = list_directors(int(page))
            else:
                params['directors'] = search_directors(int(page), params['name'])
        elif request.method == 'POST':
            page = 0
            params['name'] = request.POST.get('searchDirectorName')
            params['directors'] = search_directors(page, params['name'])
        page = int(page)
        params['previous_page'] = page - 1 if page > 0 else None
        params['next_page'] = page + 1 if len(params['directors']) == 30 else None
        return render(request, 'pages/directors.html', params)
    return redirect(home)


def actors(request):
    if request.method == 'GET' or request.method == 'POST':
        params = {'name': request.GET.get('searchActorName')}
        if request.method == 'GET':
            page = request.GET.get('page')
            if page == None or params['name'] is None:
                if page == None:
                    page = 0
                params['name'] = ""
                params['actors'] = list_actors(int(page))
            else:
                params['actors'] = search_actors(int(page), params['name'])
        elif request.method == 'POST':
            page = 0
            params['name'] = request.POST.get('searchActorName')
            params['actors'] = search_actors(page, params['name'])
        page = int(page)
        params['previous_page'] = page - 1 if page > 0 else None
        params['next_page'] = page + 1 if len(params['actors']) == 30 else None
        return render(request, 'pages/actors.html', params)
    return redirect(home)


def person(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        if name == None:
            return redirect(home)
        directorof, castof = person_detail(name)
        params = {'name': name, 'directorof': directorof, 'castof': castof}
        return render(request, 'pages/person.html', params)
    return redirect(home)
