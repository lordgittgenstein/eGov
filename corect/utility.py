from datetime import datetime
import random
import string
from corect.models import Officer, Location, Office, Complaint, History

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_group(user_id):
    return Officer.objects.get(user=user_id).type

def get_higher_office(office):
    officer = Officer.objects.get(id=office.head.id)
    boss = Officer.objects.get(id=officer.boss.id)
    return Office.objects.get(head=boss.id)

def get_offices_in(location):
    queryset = Location.objects.none()
    if location.type == 'state' or location.type == 'ut':
        queryset = Location.objects.filter(state=location.state)
    if location.type == 'division':
        queryset = Location.objects.filter(division=location.division)
    if location.type == 'district':
        queryset = Location.objects.filter(district=location.district)
    if location.type == 'subdistrict':
        queryset = Location.objects.filter(subdistrict=location.subdistrict)
    if location.type == 'locality' or location.type == 'village':
        queryset = Location.objects.filter(locality=location.locality)
    office_list = Office.objects.none()
    for q in queryset:
        office_list = office_list | Office.objects.filter(location=q.id)
    return office_list

def get_offices_over(location):
    queryset = Location.objects.none()
    aqueryset = Location.objects.none()
    flag = 'dont'
    if location.type == 'state' or location.type == 'ut':
        queryset = Location.objects.filter(state=location.state) 
    if location.type == 'division':
        aqueryset = Location.objects.filter(state=location.state)
        queryset = Location.objects.filter(division=location.division)
    if location.type == 'district':
        aqueryset = Location.objects.filter(division=location.division)
        queryset = Location.objects.filter(district=location.district)
        flag = 'do'
    if location.type == 'subdistrict':
        aqueryset = Location.objects.filter(district=location.district)
        queryset = Location.objects.filter(subdistrict=location.subdistrict)
        flag = 'do'
    if location.type == 'locality' or location.type == 'village':
        aqueryset = Location.objects.filter(subdistrict=location.subdistrict)
        queryset = Location.objects.filter(locality=location.locality)
        flag = 'do'
    office_list = Office.objects.none()
    if flag == 'do':
        for q in aqueryset:
            office_list = office_list | Office.objects.filter(location=q.id)
    for q in queryset:
        office_list = office_list | Office.objects.filter(location=q.id)
    return office_list

def get_complaints_under(officer):
    officers_under = Officer.objects.filter(boss=officer.id)
    offices = Office.objects.none()
    for o in officers_under:
        offices = offices | Office.objects.filter(head=o.id)
    complaints_under = Complaint.objects.none()
    for oo in offices:
        complaints_under = complaints_under | Complaint.objects.filter(office=oo.id)
    complaints = Complaint.objects.filter(office=Office.objects.get(head=officer.id).id)
    return complaints | complaints_under

def n_deadlines(officer):
    officers_under = Officer.objects.filter(boss=officer.id)
    offices = Office.objects.none()
    for o in officers_under:
        offices = offices | Office.objects.filter(head=o.id)
    n_complaints_under = 0
    for oo in offices:
        n_complaints_under = n_complaints_under + Complaint.objects.filter(
                                                    office=oo.id,
                                                    wake_up__lte=datetime.now().date(),
                                                    resolved=False).count()
    n_complaints = Complaint.objects.filter(office=Office.objects.get(
                                                    head=officer.id).id,
                                                    wake_up__lte=datetime.now().date(),
                                                    resolved=False).count()
    return n_complaints + n_complaints_under

def n_recent(officer, last_login):
    complaints, n_events = get_complaints_under(officer), 0        
    for c in complaints:
        if c.office.id == Office.objects.get(head=officer.id).id:
            n_events = n_events + History.objects.filter(complaint=c.id,
                                    datetime__gte=datetime.combine(last_login, datetime.min.time()),
                                    is_read_officer=False).exclude(user=officer.user).count()
        else:
            n_events = n_events + History.objects.filter(
                                    complaint=c.id,
                                    datetime__gte=datetime.combine(last_login, datetime.min.time()),
                                    is_read_boss=False).exclude(user=officer.user).count()
    return n_events