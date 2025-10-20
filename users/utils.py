from django.db.models import Q
from .models import Skill,Profile
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

def searchProfile(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles= Profile.objects.distinct().filter(
        Q(name__icontains= search_query)|
        Q(short_intro__icontains= search_query)|
        Q(skill__name__icontains=search_query)
    ).order_by('name')


    return profiles,search_query


def paginatorProfiles(request,profiles,results):

    page = request.GET.get('page',1)

    try :
        page = int (page)

    except:
        page = 1

    paginator =  Paginator(profiles,results)

    try:
       profiles = paginator.page(page)

    except PageNotAnInteger:
        page =1 
        profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    totalpages = paginator.num_pages
    endpages = list(range(max(totalpages-4,1),totalpages+1))

    if page <5:
        startpages = list(range(1,min(6,totalpages-4)))
    else:
        startpages = [1,page-2 ,page-1 ,page , page+1 , page+2]

    customrange = startpages+endpages

    customrange = sorted(set([n for n in customrange if 1<= n <=totalpages]))

    return customrange , profiles