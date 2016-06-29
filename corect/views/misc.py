from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def leave(request):
    logout(request)
    return HttpResponseRedirect('/corect')

error_map = {1:'Already saved in database.'}
@never_cache
def error(request, error_code=0):
    if error_code: return render(request, 'corect/error.html', {'error_text':error_map[error_code]})
    return render(request, 'corect/error.html', {'error_text':'Error! -- o_o -- !'})

@never_cache
def openlist(request, page=0):
    context = {'user':request.user, 'logged_in':'false', 'registered':'false'}
    if not request.user.is_anonymous(): context['logged_in'], context['registered'] = 'true', 'true'
    return render(request, 'corect/openlist.html', context)
