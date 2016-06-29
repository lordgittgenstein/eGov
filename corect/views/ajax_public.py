from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from corect.forms import make_form_a, CorrespondForm
from corect.models import Location, Complaint
from eGov.settings import LIST_SIZE, PAGE_WINDOW


@never_cache
def ajax_openlist(request, page=0):
    page = int(page)
    complaints = Complaint.objects.filter(confidential=False)
    context = {'complaints':complaints}
    if not complaints.count(): context['empty_list'] = 'empty_list'
    
    if complaints.count() <= LIST_SIZE or page == 0: context['total_pages'] = 1
    else:        
        paged_data = Paginator(complaints, LIST_SIZE)
        context['complaints'] = paged_data.page(page)
        if paged_data.page(page).has_next(): context['next_link'] = page + 1
        if paged_data.page(page).has_previous(): context['previous_link'] = page - 1
        context['page'] = page
        context['total_pages'] = paged_data.num_pages
        if paged_data.num_pages < 2 * PAGE_WINDOW:
            context['range'] = range(page - PAGE_WINDOW / 2, page + PAGE_WINDOW / 2 + 1)
        else: context['range'] = range(page - PAGE_WINDOW, page + PAGE_WINDOW + 1)
    
    return render(request, 'corect/ajax/ajax_openlist.html', context)

@csrf_exempt
@never_cache
def ajax_locations_under(request):
    context = {}
    if request.POST['type'] == 'division':
        locations = Location.objects.filter(division=request.POST['value'], type='district')
        context['district'] = 'district'
    elif request.POST['type'] == 'district':
        locations = Location.objects.filter(district=request.POST['value'], type='subdistrict')
        context['subdistrict'] = 'subdistrict'
    elif request.POST['type'] == 'subdistrict':
        locations = Location.objects.filter(subdistrict=request.POST['value'], type='locality')
        context['locality'] = 'locality'
    else:
        locations = Location.objects.all()
        context['error'] = 'error'
    context['locations'] = locations
    return render(request, 'corect/ajax/ajax_locations_under.html', context)

@never_cache
def ajax_form_a1(request):
    LocationForm = make_form_a()
    return render(request, 'corect/ajax/ajax_form_a1.html', {'form': LocationForm() })

@never_cache
def ajax_form_a2(request):
    return render(request, 'corect/ajax/ajax_form_a2.html', {'form': CorrespondForm() })

@never_cache
def ajax_form_check(request):
    return render(request, 'corect/ajax/ajax_form_check.html', {'form': CorrespondForm() })
