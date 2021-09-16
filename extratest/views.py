from django.http.response import HttpResponseRedirect
from django.shortcuts import render 
from django.views import View
from django.urls import reverse
from extratest.services import (ExtracenseList, SessionStorage)


session_store = SessionStorage()

class ChooseNumberOfExtrasensesView(View):

    def get(self, request):
        return render(request, 'start.html')
    
    def post(self, request):
        
        list_of_extrasenses = ExtracenseList()
        list_of_extrasenses.create_n_extrasenses_in_list(
            n = int(request.POST.get("num_of_extrasenses", 2))
        )
        session_store.save(
            session_key = request.session.session_key,
            extrasense_list = list_of_extrasenses,
            my_numbers = []
            )

        return HttpResponseRedirect(reverse('maingame_first_window_url'))

class MainGameFirstWindowView(View):
    
    def get(self, request):

        try:
            extrasense_list = session_store.load_extrasense(request.session.session_key)
            my_numbers = session_store.load_my_numbers(request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        ctx = { 'extrasenses' : [], 'my_numbers': my_numbers }

        for ex in extrasense_list:
            ctx['extrasenses'].append({
                'numbers' : ex.numbers,
                'rating' : ex.rating
            })
        
        return  render(request, 'index.html', context=ctx)

    def post(self, request):

        try:
            extrasense_list = session_store.load_extrasense(request.session.session_key)
            my_numbers = session_store.load_my_numbers(request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        for ex in extrasense_list:
           ex.new_number()
        
        session_store.save(
            session_key = request.session.session_key,
            extrasense_list = extrasense_list,
            my_numbers = my_numbers
            )

        return HttpResponseRedirect(reverse('maingame_second_window_url'))


class MainGameSecondWindowView(View):
    
    def get(self, request):

        try:
            extrasense_list = session_store.load_extrasense(request.session.session_key)
            my_numbers = session_store.load_my_numbers(request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        ctx = { 'extrasenses' : [], 'my_numbers': my_numbers }

        for ex in extrasense_list:
            ctx['extrasenses'].append({
                'numbers' : ex.numbers,
                'rating' : ex.rating
            })

        return render(request, 'index2.html', context=ctx)

    def post(self, request):

        entered_number = int(request.POST.get('my_number'))
        
        try:
            extrasense_list = session_store.load_extrasense(request.session.session_key)
            my_numbers = session_store.load_my_numbers(request.session.session_key)
        except KeyError:
            return HttpResponseRedirect(reverse('start_url'))

        for ex in extrasense_list:
           ex.check_last_number(entered_number)
        my_numbers.append(entered_number)

        session_store.save(
            session_key = request.session.session_key,
            extrasense_list = extrasense_list,
            my_numbers = my_numbers
            )

        return HttpResponseRedirect(reverse('maingame_first_window_url'))