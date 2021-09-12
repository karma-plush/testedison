from django.shortcuts import render
from django.views import View
from .extrasense import Extrasense


class MainView(View):

    ex1 = Extrasense()
    ex2 = Extrasense()
    mynums = []

    def get(self, request, *args, **kwargs):

        request.session.set_expiry(0)

        request.session['ex1_nums'] = self.ex1.numbers
        request.session['ex2_nums'] = self.ex2.numbers
        request.session['ex1_rating'] = self.ex1.rating
        request.session['ex2_rating'] = self.ex2.rating
        request.session['mynums'] = self.mynums
        
        return render(request, 'index.html', context={
            'ex1_nums':  request.session['ex1_nums'],
            'ex2_nums': request.session['ex2_nums'],
            'ex1_rating': request.session['ex1_rating'],
            'ex2_rating': request.session['ex2_rating'],
            'mynums': request.session['mynums']
        })

    def post(self, request, *args, **kwargs):

        if 'ready' in request.POST:
            self.ex1.new_number()
            self.ex2.new_number()
            self.mynums.append('-')
          
            request.session['ex1_nums'] = self.ex1.numbers
            request.session['ex2_nums'] = self.ex2.numbers
            request.session['mynums'] = self.mynums
            request.session.modified = True

            return render(request, 'index2.html', context={
                'ex1_nums':  request.session['ex1_nums'],
                'ex2_nums': request.session['ex2_nums'],
                'ex1_rating': request.session['ex1_rating'],
                'ex2_rating': request.session['ex2_rating'],
                'mynums': request.session['mynums']
            })

        if 'entered' in request.POST:

            number = int(request.POST.get('my_number'))

            self.mynums[-1] = number

            request.session['mynums'] = self.mynums
            request.session.modified = True

            if number == self.ex1.last_number():
                self.ex1.rateup()
                self.ex2.ratedown()
            elif number == self.ex2.last_number():
                self.ex2.rateup()
                self.ex1.ratedown()
            else:
                self.ex1.ratedown()
                self.ex2.ratedown()

            request.session['ex1_nums'] = self.ex1.numbers
            request.session['ex2_nums'] = self.ex2.numbers
            request.session['ex1_rating'] = self.ex1.rating
            request.session['ex2_rating'] = self.ex2.rating
            request.session['mynums'] = self.mynums
            request.session.modified = True

            return render(request, 'index.html', context={
                'ex1_nums':  request.session['ex1_nums'],
                'ex2_nums': request.session['ex2_nums'],
                'ex1_rating': request.session['ex1_rating'],
                'ex2_rating': request.session['ex2_rating'],
                'mynums': request.session['mynums']
            })