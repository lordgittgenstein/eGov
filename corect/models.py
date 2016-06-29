from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    title = models.CharField(max_length=200, verbose_name='Subject')
    body = models.CharField(max_length=2000, verbose_name='Details')
    office = models.ForeignKey('Office')
    name = models.CharField(max_length=200, verbose_name='Complainant Name')
    phone = models.CharField(max_length=11, default='', blank=True)
    email = models.EmailField(max_length=254, default='', blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d', blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=10, blank=True, null=True)
    confidential = models.BooleanField(default=True, verbose_name='Hidden from public view')
    resolved = models.BooleanField(default=False)
    is_read_officer = models.BooleanField(default=False)
    is_read_boss = models.BooleanField(default=False)
    wake_up = models.DateField(default='3000-01-01', blank=True, null=True)

    def __unicode__(self):
        return str(self.id) + ' ' + str(self.title)

class Branch(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey('Location')
    head = models.ForeignKey('Officer')

    def __unicode__(self):
        return str(self.name) + ', ' + str(self.location)

class Office(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey('Location')
    head = models.ForeignKey('Officer')
    branch = models.ForeignKey('Branch')

    def __unicode__(self):
        return str(self.name) + ', ' + str(self.location) 

class Officer(models.Model):
    designation = models.CharField(max_length=400)
    location = models.ForeignKey('Location')
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(User)
    boss = models.ForeignKey('self')
    type = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.designation) + ', ' + str(self.location)

class History(models.Model):
    complaint = models.ForeignKey('Complaint')
    event = models.CharField(max_length=200)
    detail = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    is_read_officer = models.BooleanField(default=False)
    is_read_boss = models.BooleanField(default=False)
    is_read_complainee = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id) + ' ' + str(self.event)

class Message(models.Model):
    text = models.CharField(max_length=1000, verbose_name='Comment')
    complaint = models.ForeignKey('Complaint')
    user = models.ForeignKey(User)
    is_read_officer = models.BooleanField(default=False)
    is_read_boss = models.BooleanField(default=False)
    is_read_complainee = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id) + ' ' + str(self.datetime)
    
class Location(models.Model):
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200, default='', blank=True)
    division = models.CharField(max_length=200, default='', blank=True)
    district = models.CharField(max_length=200, default='', blank=True)
    subdistrict = models.CharField(max_length=200, default='', blank=True, verbose_name='City/Block/Tehsil')
    locality = models.CharField(max_length=200, default='', blank=True, verbose_name='Locality/Village')
    type = models.CharField(max_length=50)

    def __unicode__(self):
        location = self.state
        if self.state == '': return 'Not Specified'
        else: location = location
        if self.division == '': return location
        else: location = self.division + ' Division, ' + location
        if self.district == '': return location
        else: location = self.district + ' District'
        if self.subdistrict == '': return location
        else: location = self.subdistrict + ', ' + location
        if self.locality == '': return location
        else: location = self.locality + ', ' + location