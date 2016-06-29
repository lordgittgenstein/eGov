from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from corect.models import Officer, Office, Complaint, History
from corect.utility import get_complaints_under
from eGov.settings import LIST_SIZE, PAGE_WINDOW

@login_required
@never_cache
def ajax_home(request, page=0):    
    officer = Officer.objects.get(user=request.user.id)
    office = Office.objects.get(head=officer.id)
    context, page = {'user':request.user}, int(page)
    complaints = Complaint.objects.filter(office=office.id, resolved=False)
    new_complaints = Complaint.objects.filter(office=office.id, resolved=False,
                                              is_read_officer=False).count()
    context['n_complaints'] = complaints.count()
    context['complaints'] = complaints
    context['new_complaints'] = new_complaints

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

    if not complaints.count(): context['empty_list'] = 'empty_list'
    return render(request, 'corect/ajax/ajax_home.html', context)  

@login_required
@never_cache
def ajax_subordinates(request, page=0):    
    officer = Officer.objects.get(user=request.user.id)
    subordinates = Officer.objects.filter(boss=officer.id)
    context, page = {'user':request.user}, int(page)

    n_subcomplaints, new_subcomplaints = 0, 0
    subcomplaints = Complaint.objects.none()
    for s in subordinates:
        suboffice = Office.objects.get(head=s.id)
        subcomplaints = subcomplaints | Complaint.objects.filter(office=suboffice.id, resolved=False)
        new_subcomplaints += Complaint.objects.filter(office=suboffice.id,
                                                      resolved=False, is_read_boss=False).count()
        n_subcomplaints += Complaint.objects.filter(office=suboffice.id, resolved=False).count()

    context['n_subcomplaints'] = n_subcomplaints
    context['subcomplaints'] = subcomplaints
    context['new_subcomplaints'] = new_subcomplaints

    if n_subcomplaints <= LIST_SIZE or page == 0: context['total_pages'] = 1
    else:        
        paged_data = Paginator(subcomplaints, LIST_SIZE)
        context['subcomplaints'] = paged_data.page(page)
        if paged_data.page(page).has_next(): context['next_link'] = page + 1
        if paged_data.page(page).has_previous(): context['previous_link'] = page - 1
        context['page'] = page
        context['total_pages'] = paged_data.num_pages
        if paged_data.num_pages < 2 * PAGE_WINDOW:
            context['range'] = range(page - PAGE_WINDOW / 2, page + PAGE_WINDOW / 2 + 1)
        else: context['range'] = range(page - PAGE_WINDOW, page + PAGE_WINDOW + 1)

    if not subcomplaints.count(): context['empty_list'] = 'empty_list'
    return render(request, 'corect/ajax/ajax_subordinates.html', context)

@login_required
@never_cache
def ajax_recent(request, page=0):
    page = int(page)
    complaints = get_complaints_under(Officer.objects.get(user=request.user.id))
    officer_id = Office.objects.get(head=Officer.objects.get(user=request.user.id)).id
    time_from = datetime.combine(request.user.last_login, datetime.min.time())   
    events = History.objects.none()    
    for c in complaints:
        if c.office.id == officer_id:
            addendum = History.objects.filter(complaint=c.id, datetime__gte=time_from,
                                is_read_officer=False).exclude(user=request.user.id)
        else: addendum = History.objects.filter(complaint=c.id, datetime__gte=time_from,
                                is_read_boss=False).exclude(user=request.user.id)
        if addendum.count(): events = events | addendum
    context = {}
    if not events.count(): context['empty_list'] = 'empty_list'
    else:
        if events.count() <= LIST_SIZE or page == 0:
            context['events'] = events
            context['total_pages'] = 1
        else:        
            paged_data = Paginator(events, LIST_SIZE)
            context['events'] = paged_data.page(page)
            if paged_data.page(page).has_next(): context['next_link'] = page + 1
            if paged_data.page(page).has_previous(): context['previous_link'] = page - 1
            context['page'] = page
            context['total_pages'] = paged_data.num_pages
            if paged_data.num_pages < 2 * PAGE_WINDOW:
                context['range'] = range(page - PAGE_WINDOW / 2, page + PAGE_WINDOW / 2 + 1)
            else: context['range'] = range(page - PAGE_WINDOW, page + PAGE_WINDOW + 1)

    return render(request, 'corect/ajax/ajax_recent.html', context)

@login_required
@never_cache
def ajax_mydeadlines(request, page=0):
    page = int(page)
    officer = Officer.objects.get(user=request.user.id)
    complaints = Complaint.objects.filter(office=Office.objects.get(head=officer.id).id,
                                                wake_up__lte=datetime.now().date(),
                                                resolved=False)

    context = {'complaints':complaints}
    if not complaints.count(): context = {'empty_mydeadlines':'empty_mydeadlines'}
    else:
        if complaints.count() <= LIST_SIZE / 2 or page == 0: context['my_total_pages'] = 1
        else:        
            paged_data = Paginator(complaints, LIST_SIZE / 2)
            context['complaints'] = paged_data.page(page)
            if paged_data.page(page).has_next(): context['my_next_link'] = page + 1
            if paged_data.page(page).has_previous(): context['my_previous_link'] = page - 1
            context['my_page'] = page
            context['my_total_pages'] = paged_data.num_pages
            if paged_data.num_pages < 2 * PAGE_WINDOW:
                context['my_range'] = range(page - PAGE_WINDOW / 2, page + PAGE_WINDOW / 2 + 1)
            else: context['my_range'] = range(page - PAGE_WINDOW, page + PAGE_WINDOW + 1)
    return render(request, 'corect/ajax/ajax_mydeadlines.html', context)

@login_required
@never_cache
def ajax_subdeadlines(request, page=0):
    page = int(page)
    officer = Officer.objects.get(user=request.user.id)
    officers_under = Officer.objects.filter(boss=officer.id)
    offices = Office.objects.none()
    for o in officers_under:
        offices = offices | Office.objects.filter(head=o.id)

    complaints_under = Complaint.objects.none()
    for oo in offices:
        addendum = Complaint.objects.filter(office=oo.id, wake_up__lte=datetime.now().date(), resolved=False)
        if addendum.count(): complaints_under = complaints_under | addendum

    context = {'subcomplaints':complaints_under}
    if not complaints_under.count(): context = {'empty_subdeadlines':'empty_subdeadlines'}
    else:
        if complaints_under.count() <= LIST_SIZE / 2 or page == 0: context['sub_total_pages'] = 1
        else:        
            paged_data = Paginator(complaints_under, LIST_SIZE / 2)
            context['subcomplaints'] = paged_data.page(page)
            if paged_data.page(page).has_next(): context['sub_next_link'] = page + 1
            if paged_data.page(page).has_previous(): context['sub_previous_link'] = page - 1
            context['sub_page'] = page
            context['sub_total_pages'] = paged_data.num_pages
            if paged_data.num_pages < 2 * PAGE_WINDOW:
                context['sub_range'] = range(page - PAGE_WINDOW / 2, page + PAGE_WINDOW / 2 + 1)
            else: context['sub_range'] = range(page - PAGE_WINDOW, page + PAGE_WINDOW + 1)
    return render(request, 'corect/ajax/ajax_subdeadlines.html', context)

@login_required
@never_cache
def ajax_search(request, string=''):
    if not string : return HttpResponse()
    if len(string) < 3: return HttpResponse()

    officer = Officer.objects.get(user=request.user.id)
    office = Office.objects.get(head=officer.id)
    complaints = Complaint.objects.filter(office=office.id, resolved=False,
                                          title__icontains=string) | \
                 Complaint.objects.filter(office=office.id, resolved=False,
                                          body__icontains=string) | \
                 Complaint.objects.filter(office=office.id, resolved=False,
                                          name__icontains=string)

    subordinates = Officer.objects.filter(boss=officer.id)
    subcomplaints = Complaint.objects.none()
    for s in subordinates:
        suboffice = Office.objects.get(head=s.id)
        subcomplaints = subcomplaints | \
                        Complaint.objects.filter(office=suboffice.id, resolved=False,
                                                    title__icontains=string) | \
                        Complaint.objects.filter(office=suboffice.id, resolved=False,
                                                    body__icontains=string) | \
                        Complaint.objects.filter(office=suboffice.id, resolved=False,
                                                    name__icontains=string)

    table = complaints | subcomplaints
    context = {'table':table[:9], 'string':string}
    return render(request, 'corect/ajax/ajax_search.html', context)
