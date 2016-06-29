from datetime import datetime
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from corect.forms import make_form_a, make_form_b, BlankComplaintForm, \
    CorrespondForm, MessageForm, ChangeKeyForm, ChangeContactForm
from corect.models import Location, Complaint, History, Office, Message
from corect.utility import id_generator, get_higher_office
from corect.views import error
from eGov.settings import WAIT_DAYS

@never_cache
def form_a(request):
    try:
        if request.session['has_key'] == True: 
            return HttpResponseRedirect('/corect/check/' + str(request.session['complaint_number']))
    except: pass
    LocationForm = make_form_a()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            l = Location()
            if request.POST['state']:
                l = Location.objects.filter(state=form.cleaned_data['state'])
                if request.POST['division']:
                    l = Location.objects.filter(
                            state=form.cleaned_data['state'],
                            division=form.cleaned_data['division'])
                    if request.POST['district']:
                        l = Location.objects.filter(
                                state=form.cleaned_data['state'],
                                division=form.cleaned_data['division'],
                                district=form.cleaned_data['district'])
                        if request.POST['subdistrict']:
                            l = Location.objects.filter(
                                state=form.cleaned_data['state'],
                                division=form.cleaned_data['division'],
                                district=form.cleaned_data['district'],
                                subdistrict=form.cleaned_data['subdistrict'])
                            if request.POST['locality']:
                                l = Location.objects.filter(
                                    state=form.cleaned_data['state'],
                                    division=form.cleaned_data['division'],
                                    district=form.cleaned_data['district'],
                                    subdistrict=form.cleaned_data['subdistrict'],
                                    locality=form.cleaned_data['locality'])
            return form_b(request, l[0])
    else: form = LocationForm()
    context = {'form': form, 'logged_in':'false', 'registered':'false'}
    return render(request, 'corect/form_a.html', context)

@never_cache
def form_b(request, location=Location.objects.get(pk=1)):
    ComplaintForm = make_form_b(location)
    try:
        if request.method == 'POST' and request.POST['submit_for_form_b'] == 'Next >':
            return render(request, 'corect/form_b.html', {'form':ComplaintForm(), 'l':location,
                                                          'logged_in':'false', 'registered':'false'})
    except: pass
    if request.method == 'POST':
        form = BlankComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            comp = Complaint()
            comp.title = form.cleaned_data['title']
            comp.body = form.cleaned_data['body']
            comp.office = form.cleaned_data['office']
            comp.confidential = form.cleaned_data['confidential']
            comp.name = form.cleaned_data['name']
            comp.email = form.cleaned_data['email']
            comp.document = form.cleaned_data['document']           
            comp.key = id_generator()
            comp.phone = ''
            if form.cleaned_data['phone']: comp.phone = form.cleaned_data['phone']
            if Complaint.objects.filter(
                    title=comp.title,
                    body=comp.body,
                    office=comp.office,
                    name=comp.name).count():
                return error(request)
            comp.save()
            log = History()
            log.complaint = comp
            log.event = 'lodged complaint'
            log.detail = form.cleaned_data['title']
            log.datetime = comp.datetime
            log.is_read_complainee = True 
            log.user = User.objects.get(username='complainee')
            log.save()
            context = {'form':form, 'compid':comp.id, 'key':comp.key}
            return render(request, 'corect/report.html', context)
    else: form = ComplaintForm()
    context = {'form': form, 'l':location, 'logged_in':'false', 'registered':'false'}
    return render(request, 'corect/form_b.html', context)

@never_cache
def detail_anonymous(request, complaint_id):
    complaint = Complaint.objects.get(pk=complaint_id)
    history = History.objects.filter(complaint=complaint_id)
    office = Office.objects.filter(id=complaint.office.id)
    period = datetime.now().date() - complaint.datetime.date()
    if period.days < WAIT_DAYS: message = 'Track'
    else: message = 'Forward'
    
    context = {'complaint':complaint,
               'message': message,
               'officer':office[0].head,
               'history':history,
               'no_button':'no_button',
               'registered':'false'}
    try:
        if request.session['has_key'] == True: context['logged_in'] = 'true'
    except:
        request.session['has_key'] = False
        context['logged_in'] = 'false'

    if complaint.confidential == True:
            if request.session['has_key'] == False: return error(request)
    if request.session['has_key'] == True:
        u = User.objects.filter(username='complainee')
        for h in history:
            h.is_read_complainee = True
            h.save()
    else:
        context['comment_disabled'] = True
        u = User.objects.filter(username='anonymous')
    if request.method == 'POST':
        form2 = MessageForm(request.POST)
        if form2.is_valid():
            msg = Message()
            msg.text = form2.cleaned_data['text']
            msg.user = u[0]
            msg.complaint = complaint
            if len(msg.text) != 0 and not msg.text.isspace():
                msgs = Message.objects.filter(complaint_id=complaint_id)
                log = History()
                log.complaint = complaint
                log.event = 'posted comment'
                log.detail = msg.text
                log.user = User.objects.get(username='complainee')
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

@never_cache
def check(request):
    try:
        if request.session['has_key'] == True:
            return HttpResponseRedirect(str(request.session['complaint_number']))
    except: pass
    if request.method == 'POST':
        form = CorrespondForm(request.POST)
        if form.is_valid():
            try:
                key = Complaint.objects.get(pk=int(form.cleaned_data['number'])).key
                if str(form.cleaned_data['key']) == str(key):
                    request.session['has_key'] = True
                    request.session['complaint_number'] = form.cleaned_data['number']
                    return HttpResponseRedirect(str(form.cleaned_data['number']))
            except: error(request)
        else:
            context = {'form': CorrespondForm(),
                       'logged_in':'false',
                       'registered':'false',
                       'error_message':'Complaint Number and Valid Key must be entered.'}
            return render(request, 'corect/check.html', context)

    context = {'form': CorrespondForm(), 'logged_in':'false', 'registered':'false'}
    return render(request, 'corect/check.html', context)

@never_cache
def refer(request):
    alright = 'no'
    try:
        if request.session['has_key'] == True:
            complaint = Complaint.objects.get(id=request.session['complaint_number'])
            alright = 'yes'
    except:
        if request.method == 'POST':
            form = CorrespondForm(request.POST)
            if form.is_valid():
                try:
                    key = Complaint.objects.get(pk=int(form.cleaned_data['number'])).key
                    if str(form.cleaned_data['key']) == str(key):
                        request.session['has_key'] = True
                        request.session['complaint_number'] = form.cleaned_data['number']
                except: error(request)
                complaint = Complaint.objects.get(id=form.cleaned_data['number'])
                alright = 'yes'
    
    if alright == 'yes':
        exists = 'Dont know'
        boss_office = get_higher_office(Office.objects.get(id=complaint.office.id))
        new_body = complaint.name + ' forwared older complaint due to inaction: {' + complaint.body + '}'
        new_title = 'Inaction: ' + complaint.title
        if Complaint.objects.filter(title=new_title, body=new_body, office=boss_office,
                                    name=complaint.name).count(): exists = 'Exists'
        period = datetime.now().date() - complaint.datetime.date()
        if period.days < WAIT_DAYS: message = 'Track'
        else: message = 'Forward'
        context = {'complaint':complaint, 'logged_in':'true', 'registered':'false',
                   'message':message, 'exists':exists}
        return render(request, 'corect/refer.html', context)
    else:  return render(request, 'corect/forward.html', {'form': CorrespondForm(),
                                                          'logged_in':'true',
                                                          'registered':'false'})

@never_cache
def forward(request, complaint_id):
    try:
        if request.session['has_key'] == False: return error(request)
    except: pass    
    complaint = Complaint.objects.get(id=complaint_id)
    boss_office = get_higher_office(Office.objects.get(id=complaint.office.id))
    new_body = complaint.name + ' forwared older complaint due to inaction: {' + complaint.body + '}'
    new_title = 'Inaction: ' + complaint.title
    nc = Complaint()
    nc.title = new_title
    nc.body = new_body
    nc.office = boss_office
    nc.name = complaint.name
    nc.phone = complaint.phone
    nc.email = complaint.email
    nc.document = complaint.document
    nc.datetime = str(datetime.now())
    nc.key = complaint.key
    nc.confidential = complaint.confidential
    if Complaint.objects.filter(title=new_title, body=new_body, office=boss_office,
                                name=complaint.name).count(): return error(request, 1)
    nc.save()
    history = History.objects.filter(complaint=complaint)
    for h in history:
        log = History()
        log = h 
        log.save()
    log = History()
    log.complaint = nc
    log.event = 'forwarded complaint'
    log.detail = nc.title
    log.datetime = nc.datetime
    log.user = User.objects.get(username='complainee')
    log.save()
    return render(request, 'corect/report_b.html', {'complaint':complaint,
                                                    'newid':nc.id,
                                                    'logged_in':'true',
                                                    'registered':'false'})

@never_cache
def change_key(request):
    try:
        if not request.session['has_key']: return error(request)
    except: pass
    complaint = Complaint.objects.get(id=request.session['complaint_number'])
    period = datetime.now().date() - complaint.datetime.date()
    if period.days < WAIT_DAYS: message = 'Track'
    else: message = 'Forward'
    context = {'complaint':complaint,
               'form': ChangeKeyForm(old_key=complaint.key, data=None),
               'logged_in':'true',
               'registered':'false',
               'message':message}
    if request.method == 'POST':
        form = ChangeKeyForm(old_key=complaint.key, data=request.POST)
        if form.is_valid():
            complaint.key = form.cleaned_data['new']
            complaint.save()
            return render(request, 'corect/success.html', context)
        else:
            context['error'] = 'Enter the new key twice, exactly the same, to change.'
    return render(request, 'corect/change_key.html', context)

@never_cache
def change_contact(request):
    try:
        if not request.session['has_key']: return error(request)
    except: pass
    complaint = Complaint.objects.get(id=request.session['complaint_number'])
    period = datetime.now().date() - complaint.datetime.date()
    if period.days < WAIT_DAYS: message = 'Track'
    else: message = 'Forward'
    context = {'complaint':complaint,
               'form': ChangeContactForm(old_key=complaint.key, data=None),
               'logged_in':'true',
               'registered':'false',
               'message':message}
    if request.method == 'POST':
        form = ChangeContactForm(old_key=complaint.key, data=request.POST)
        if form.is_valid():
            complaint.phone = form.cleaned_data['phone']
            complaint.email = form.cleaned_data['email']
            complaint.save()
            return render(request, 'corect/success.html', context)
        else:
            context['error'] = 'Enter your working mobile phone number or currect email id.'
    return render(request, 'corect/change_contact.html', context)
