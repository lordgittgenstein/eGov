from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from corect.forms import MarkingForm, DateInputForm, MessageForm, \
    HistoryFilterForm, ChangePasswordForm, ChangeDetailsForm
from corect.models import Officer, Complaint, History, Office, Message
from corect.utility import n_deadlines, n_recent, get_group
from corect.views import error
from eGov.settings import HISTORY_PAD, MAX_HISTORY_SIZE


@never_cache
def index(request):
    print make_password('pass', salt=None, hasher='default')
    if request.user.is_anonymous():
        try:
            if request.session['has_key'] == True:
                return HttpResponseRedirect('/corect/check/' + str(request.session['complaint_number']))
        except: pass
    else: return HttpResponseRedirect(reverse('corect.views.home'))

    context = {'logged_in':'false', 'registered':'false'}
    if 'username' not in request.POST.keys() or 'password' not in request.POST.keys():
        return render(request, 'corect/index.html', context)
    else: option = auth(request)
    if option == 'no_error': return HttpResponseRedirect(reverse('corect.views.home'))
    else:
        context['error'] = 'Error: Enter correct Username-Password.'
        return render(request, 'corect/index.html', context)
    
def auth(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return 'no_error'
    else: return 'error'

@login_required
@never_cache
def home(request, pick='all', page=0):
    officer = Officer.objects.get(user=request.user.id)
                                              
    return render(request, 'corect/home.html',
                {'user':request.user,
                 'logged_in':'true',
                 'registered':'true',
                 'n_deadlines': n_deadlines(officer),
                 'n_recent': n_recent(officer, request.user.last_login)})

@login_required
@never_cache
def subordinates(request, pick='all', page=0):    
    officer = Officer.objects.get(user=request.user.id)
    return render(request, 'corect/subordinates.html',
                  {'user':request.user,
                   'logged_in':'true',
                   'registered':'true',
                   'n_deadlines': n_deadlines(officer),
                   'n_recent': n_recent(officer, request.user.last_login)})

@login_required
@never_cache
def history(request):
    officer = Officer.objects.get(user=request.user.id)
    complaints = Complaint.objects.filter(office=Office.objects.get(head=officer.id).id)
    officers_under = Officer.objects.filter(boss=officer.id)
    offices = Office.objects.none()
    for o in officers_under:
        offices = offices | Office.objects.filter(head=o.id)
    complaints_under = Complaint.objects.none()
    for oo in offices:
        addendum = Complaint.objects.filter(office=oo.id)
        if addendum.count(): complaints_under = complaints_under | addendum
    all_complaints = complaints | complaints_under

    form = HistoryFilterForm()
    context = {'form':form, 'logged_in':'true', 'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(officer, request.user.last_login)}
    if request.method == 'POST':
        form = HistoryFilterForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data['date_input']
            events = History.objects.none()
            for c in all_complaints:
                addendum = History.objects.filter(event=form.cleaned_data['event'],
                            datetime__lte=datetime.combine(d, datetime.min.time()) + timedelta(days=HISTORY_PAD),
                            datetime__gt=datetime.combine(d, datetime.min.time()) - timedelta(days=HISTORY_PAD),
                            complaint_id=c.id)
                if addendum.count() > MAX_HISTORY_SIZE:
                    addendum = History.objects.filter(event=form.cleaned_data['event'],
                            datetime__lte=datetime.combine(d, datetime.min.time()) + timedelta(days=1),
                            datetime__gt=datetime.combine(d, datetime.min.time()) - timedelta(days=1),
                            complaint_id=c.id)
                if addendum.count(): events = events | addendum
            context['events'] = events
            if not events.count(): context['empty_list'] = 'empty_list'
    return render(request, 'corect/history.html', context)

@login_required
@never_cache
def recent(request):
    officer = Officer.objects.get(user=request.user.id)
    context = {'logged_in':'true', 'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(officer, request.user.last_login)}
    return render(request, 'corect/recent.html', context)

@login_required
@never_cache
def deadlines(request):
    officer = Officer.objects.get(user=request.user.id)    
    context = {'logged_in':'true', 'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(officer, request.user.last_login)}
    return render(request, 'corect/deadlines.html', context)

@login_required
@never_cache
def change_profile(request):
    officer = Officer.objects.get(user=request.user.id)
    context = {'user':request.user,
               'officer':Officer.objects.get(user=request.user.id),
               'form1': ChangePasswordForm(user=request.user, data=None),
               'form2': ChangeDetailsForm(user=request.user, data=None),
               'logged_in':'true',
               'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(officer, request.user.last_login)}

    return render(request, 'corect/change_profile.html', context)

@login_required
@never_cache
def change_password(request):
    officer = Officer.objects.get(user=request.user.id)
    context = {'user':request.user,
               'officer':Officer.objects.get(user=request.user.id),
               'form': ChangePasswordForm(user=request.user, data=None),
               'logged_in':'true',
               'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(officer, request.user.last_login)}
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            u = User.objects.get(id=request.user.id)
            u.set_password(form.cleaned_data['new'])
            u.save()
            return render(request, 'corect/success.html', context)
        else:
            context['error'] = 'Enter current password. Then enter new\
             password twice, with mimimum length 8.'
    return render(request, 'corect/change_password.html', context)

@login_required
@never_cache
def change_official_contact(request):
    officer = Officer.objects.get(user=request.user.id)
    context = {'user':request.user,
               'officer':Officer.objects.get(user=request.user.id),
               'form': ChangeDetailsForm(user=request.user, data=None),
               'logged_in':'true',
               'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(officer, request.user.last_login)}
    if request.method == 'POST':
        form = ChangeDetailsForm(user=request.user, data=request.POST)
        if form.is_valid():
            o = Officer.objects.get(user=request.user.id)
            o.phone = form.cleaned_data['phone']
            o.email = form.cleaned_data['email']
            o.save()
            return render(request, 'corect/success.html', context)
        else:
            context['error'] = 'Enter current password. Then enter your working\
             mobile phone number and currect email id.'
    return render(request, 'corect/change_official_contact.html', context)

@login_required
@never_cache
def detail_officer(request, complaint_id):
    complaint = Complaint.objects.get(pk=complaint_id)
    history = History.objects.filter(complaint=complaint_id)
    office = Office.objects.get(id=complaint.office.id)
    officer = Officer.objects.get(id=office.head.id)
    viewer = Officer.objects.get(user=request.user.id)
    mform = MarkingForm()
    dform = DateInputForm()
    
    context = {'complaint':complaint,
               'officer':officer,
               'history':history,
               'mform':mform,
               'dform':dform,
               'group':get_group(request.user.id),
               'logged_in':'true',
               'registered':'true',
               'n_deadlines': n_deadlines(officer),
               'n_recent': n_recent(viewer, request.user.last_login)}

    if request.user.id == officer.user.id:
        context['is_boss'] = 'false'
        if complaint.is_read_officer == False:
            new_officer_history = []
            for h in History.objects.filter(complaint=complaint_id, is_read_officer=False):
                new_officer_history.append(h.id)
            context['new_officer_history'] = new_officer_history
            complaint.is_read_officer = True
            for h in history:
                h.is_read_officer = True
                h.save()
            log = History()
            log.complaint = complaint
            log.event = 'viewed complaint'
            log.detail = ''
            log.user = User.objects.get(id=request.user.id)
            log.is_read_officer = True
            log.datetime = datetime.now()
            log.save()    
    else:
        context['is_boss'] = 'true'        
        if complaint.is_read_boss == False:
            new_boss_history = []
            for h in History.objects.filter(complaint=complaint_id, is_read_boss=False):
                new_boss_history.append(h.id)
            context['new_boss_history'] = new_boss_history
            complaint.is_read_boss = True
            for h in history:
                h.is_read_boss = True
                h.save()
            log = History()
            log.complaint = complaint
            log.event = 'viewed complaint'
            log.detail = ''
            log.user = User.objects.get(id=request.user.id)
            log.is_read_boss = True
            log.datetime = datetime.now()
            log.save()
    complaint.save()
    if request.method == 'POST':
        form2 = MessageForm(request.POST)
        if form2.is_valid():
            msg = Message()
            msg.text = form2.cleaned_data['text']
            msg.user = request.user
            msg.complaint = complaint
            if len(msg.text) != 0 and not msg.text.isspace():
                msgs = Message.objects.filter(complaint_id=complaint_id)
                log = History()
                log.complaint = complaint
                log.event = 'posted comment'
                log.detail = msg.text
                log.user = User.objects.get(id=request.user.id)
                if request.user.id == officer.user.id: log.is_read_officer = True
                else: log.is_read_boss = True      
                log.datetime = datetime.now()
                try:
                    if msg.text != msgs[len(msgs) - 1].text:
                        msg.save()
                        log.save()
                except:
                    msg.save()
                    log.save()
    context['form2'] = MessageForm()
    context['history'] = History.objects.filter(complaint=complaint_id)
    return render(request, 'corect/detail.html', context)

@login_required
@never_cache
def mark(request, complaint_id):
    complaint = Complaint.objects.get(pk=complaint_id)
    office = Office.objects.get(pk=complaint.office.id)
    officer = Officer.objects.get(id=office.head.id)
    boss = Officer.objects.get(pk=officer.boss.id)
    if request.user.id != boss.user.id:
        return HttpResponseRedirect(reverse(detail_officer, args=[complaint_id]))
    if request.method == 'POST':
        group = get_group(request.user.id)
        if group in ['officer']:
            complaint = Complaint.objects.get(pk=complaint_id)
            try:
                if 'on' in request.POST['resolved']:
                    complaint.resolved = True
                    event = 'Resolved'
                    log = History()
                    log.complaint = complaint
                    log.event = 'marked complaint'
                    log.detail = event
                    log.datetime = datetime.now()
                    log.is_read_boss = True      
                    log.user = User.objects.get(id=request.user.id)
                    log.save()
            except: pass
            try:
                if 'on' in request.POST['unresolved']:
                    complaint.resolved = False
                    event = 'Un-resolved'
                    log = History()
                    log.complaint = complaint
                    log.event = 'marked complaint'
                    log.detail = event
                    log.datetime = datetime.now()
                    log.is_read_boss = True      
                    log.user = User.objects.get(id=request.user.id)
                    log.save()
            except: pass
            complaint.save()
        else: return error(request)
    return HttpResponseRedirect(reverse(detail_officer, args=[complaint_id]))

@login_required
@never_cache
def wake_up(request, complaint_id):    
    complaint = Complaint.objects.get(pk=complaint_id)
    office = Office.objects.get(pk=complaint.office.id)
    officer = Officer.objects.get(id=office.head.id)
    boss = Officer.objects.get(pk=officer.boss.id)    
    if request.user.id != boss.user.id:
        return HttpResponseRedirect(reverse(detail_officer, args=[complaint_id]))
    if request.method == 'POST':
        group = get_group(request.user.id)
        if group in ['officer']:
            form = DateInputForm(request.POST)
            if form.is_valid():
                comp = Complaint.objects.get(pk=complaint_id)
                comp.wake_up = form.cleaned_data['date_input']
                comp.save()
                log = History()
                log.complaint = comp
                log.event = 'set target date'
                log.detail = str(comp.wake_up.day) + '-' + str(comp.wake_up.month) + '-' + str(comp.wake_up.year) 
                log.datetime = datetime.now()
                log.is_read_boss = True      
                log.user = User.objects.get(id=request.user.id)
                log.save()
    return HttpResponseRedirect(reverse(detail_officer, args=[complaint_id]))
