from django.http.response import HttpResponseRedirect
from django.shortcuts import render 
from django.views import View
from django.urls import reverse

from extratest.services import ExtracenseList
from extratest.storage_factory import store


class ChooseNumberOfExtrasensesView(View):

    def get(self, request):

        request.session.save()
        request.session.modified = True

        return render(request, 'start.html')
    
    def post(self, request):

        list_of_extrasenses = ExtracenseList()
        list_of_extrasenses.create_n_extrasenses_in_list(
            n = int(request.POST.get("num_of_extrasenses", 2))
        )
        try:
            store.save(
                session_key = request.session.session_key,
                extrasense_list = list_of_extrasenses,
                my_numbers = []
                )
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        return HttpResponseRedirect(reverse('maingame_first_window_url'))

class MainGameFirstWindowView(View):
    
    def get(self, request):
        payload = store.load(session_key = request.session.session_key)

        ctx = {
            'extrasenses' : [],
            'my_numbers': payload['my_numbers']
            }

        for ex in payload['extrasense_list']:
            ctx['extrasenses'].append({
                'numbers' : ex.numbers,
                'rating' : ex.rating
            })
        
        return  render(request, 'index.html', context=ctx)

    def post(self, request):
        try:
            payload = store.load(session_key = request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        for ex in payload['extrasense_list']:
           ex.new_number()

        try:
            store.save(
                session_key = request.session.session_key,
                extrasense_list = payload['extrasense_list'],
                my_numbers = payload['my_numbers']
                )
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))
   

        return HttpResponseRedirect(reverse('maingame_second_window_url'))


class MainGameSecondWindowView(View):
    
    def get(self, request):

        try:
            payload = store.load(session_key = request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        ctx = {
            'extrasenses' : [],
            'my_numbers': payload['my_numbers']
            }

        for ex in payload['extrasense_list']:
            ctx['extrasenses'].append({
                'numbers' : ex.numbers,
                'rating' : ex.rating
            })

        return render(request, 'index2.html', context=ctx)

    def post(self, request):

        entered_number = int(request.POST.get('my_number'))
        
        try:
            payload = store.load(session_key = request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        for ex in payload['extrasense_list']:
           ex.check_last_number(entered_number)
        payload['my_numbers'].append(entered_number)


        try:
            store.save(
                session_key = request.session.session_key,
                extrasense_list = payload['extrasense_list'],
                my_numbers = payload['my_numbers']
                )
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        return HttpResponseRedirect(reverse('maingame_first_window_url'))