from django.http.response import HttpResponseRedirect
from django.shortcuts import render 
from django.views import View
from django.urls import reverse

from extratest.services import ExtracenseList, ExtrasenseStorage


class ChooseNumberOfExtrasensesView(View):

    def get(self, request):
        return render(request, 'start.html')
    
    def post(self, request):
        store = ExtrasenseStorage(request.session.session_key)

        list_of_extrasenses = ExtracenseList()
        list_of_extrasenses.create_n_extrasenses_in_list(
            n = int(request.POST.get("num_of_extrasenses", 2))
        )

        store.save(
            extrasense_list = list_of_extrasenses,
            my_numbers = []
            )

        return HttpResponseRedirect(reverse('maingame_first_window_url'))

class MainGameFirstWindowView(View):
    
    def get(self, request):
        store = ExtrasenseStorage(request.session.session_key)
        payload = store.load()

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
        store = ExtrasenseStorage(request.session.session_key)
        payload = store.load()

        for ex in payload['extrasense_list']:
           ex.new_number()
        
        store.save(
            extrasense_list = payload['extrasense_list'],
            my_numbers = payload['my_numbers']
            )

        return HttpResponseRedirect(reverse('maingame_second_window_url'))


class MainGameSecondWindowView(View):
    
    def get(self, request):
        store = ExtrasenseStorage(request.session.session_key)
        payload = store.load()

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
        
        store = ExtrasenseStorage(request.session.session_key)
        payload = store.load()

        for ex in payload['extrasense_list']:
           ex.check_last_number(entered_number)
        payload['my_numbers'].append(entered_number)

        store.save(
            extrasense_list = payload['extrasense_list'],
            my_numbers = payload['my_numbers']
            )

        return HttpResponseRedirect(reverse('maingame_first_window_url'))