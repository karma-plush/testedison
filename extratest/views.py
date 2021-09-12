from django.shortcuts import render
from django.views import View
from .extrasense import Extrasense

class MainView(View):

    def get(self, request, *args, **kwargs):

        ex1 = Extrasense(
            numbers=request.session.get('ex1_nums') or [],
            rating=request.session.get('ex1_rating') or 0,
        )
        ex2 = Extrasense(
            numbers=request.session.get('ex2_nums') or [],
            rating=request.session.get('ex2_rating')  or 0,
        )

        request.session['ex1_nums'] = ex1.numbers
        request.session['ex2_nums'] = ex2.numbers
        request.session['ex1_rating'] = ex1.rating
        request.session['ex2_rating'] = ex2.rating
        
        if 'mynums' not in request.session:
            request.session['mynums'] = []
        
        return render(request, 'index.html', context={
            'ex1_nums':  ex1.numbers,
            'ex2_nums': ex2.numbers,
            'ex1_rating': ex1.rating,
            'ex2_rating': ex2.rating,
            'mynums': request.session['mynums']
        })

    def post(self, request, *args, **kwargs):

        if 'ready' in request.POST:

            ex1 = Extrasense(
                numbers=request.session.get('ex1_nums'),
                rating=request.session.get('ex1_rating'),
            )
            ex2 = Extrasense(
                numbers=request.session.get('ex2_nums'),
                rating=request.session.get('ex2_rating'),
            )

            ex1.new_number()
            ex2.new_number()
            request.session['mynums'].append('-')
          
            request.session['ex1_nums'] = ex1.numbers
            request.session['ex2_nums'] = ex2.numbers
        
            request.session.modified = True

            return render(request, 'index2.html', context={
                'ex1_nums':  ex1.numbers,
                'ex2_nums': ex2.numbers,
                'ex1_rating': ex1.rating,
                'ex2_rating': ex2.rating,
                'mynums': request.session['mynums']
            })

        if 'entered' in request.POST:

            ex1 = Extrasense(
                numbers=request.session.get('ex1_nums'),
                rating=request.session.get('ex1_rating'),
            )
            ex2 = Extrasense(
                numbers=request.session.get('ex2_nums'),
                rating=request.session.get('ex2_rating'),
            )

            number = int(request.POST.get('my_number'))

            request.session['mynums'][-1] = number
            request.session.modified = True

            if number == ex1.last_number() and number == ex2.last_number():
                ex1.rateup()
                ex2.rateup()
            elif number == ex1.last_number():
                ex1.rateup()
                ex2.ratedown()
            elif number == ex2.last_number():
                ex2.rateup()
                ex1.ratedown()
            else:
                ex1.ratedown()
                ex2.ratedown()

            request.session['ex1_nums'] = ex1.numbers
            request.session['ex2_nums'] = ex2.numbers
            request.session['ex1_rating'] = ex1.rating
            request.session['ex2_rating'] = ex2.rating
            request.session.modified = True

            return render(request, 'index.html', context={
                'ex1_nums':  ex1.numbers,
                'ex2_nums': ex2.numbers,
                'ex1_rating': ex1.rating,
                'ex2_rating': ex2.rating,
                'mynums': request.session['mynums']
            })