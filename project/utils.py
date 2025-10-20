from django.db.models import Q
from .models import Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProject(request):
    search_query = request.GET.get("search_query", "")

    if search_query:
        projects = Project.objects.distinct().filter(
            Q(name__icontains=search_query)
            | Q(owner__name__icontains=search_query)
            | Q(tags__name__icontains=search_query)
        )
    else:
        projects = Project.objects.all()

    projects = projects.select_related("owner").prefetch_related("tags")

    return projects, search_query



def paginateProjects(request,projects,results):
    page = request.GET.get('page',1)
    try:
        page = int(page)
    except:
        page = 1

    paginator = Paginator(projects,results)

    try:
        projects = paginator.page(page)
    
    except PageNotAnInteger:
        page=1 
        projects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    
    totalpages= paginator.num_pages

    endpages = list(range(max(totalpages-4,1),totalpages+1))

    if page < 5 :
        startpages = list(range(1,min(6,totalpages - 4))) 
    else :
        startpages = [1,page-2,page-1,page , page+1 , page+2]
    

    customrange = startpages+endpages

    customrange =  sorted( set([n for n in customrange if  1<= n <=totalpages ]))

    return customrange , projects 