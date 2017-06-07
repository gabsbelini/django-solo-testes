import urllib.request
from bs4 import BeautifulSoup
import datetime

from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
import plotly.offline as opy
import plotly.graph_objs as go


class CafeView(TemplateView):
    def get_context_data(self, **kwargs):
        class AppURLopener(urllib.request.FancyURLopener):
            version = "Mozilla/5.0"

        opener = AppURLopener()
        response = opener.open('https://www.investing.com/commodities/us-coffee-c-contracts').read()
        soup = BeautifulSoup(response, 'html.parser')
        price = float(soup.find("td", {"class": "pid-8832-last"}).get_text())
        context = super(CafeView, self).get_context_data(**kwargs)
        context['preco'] = price
        try:
            lista_prices
        except NameError:
            lista_prices = []
        else:
            lista_prices.append(price)
        try:
            lista_hours
        except NameError:
            lista_hours = []
        else:
            lista = str(datetime.datetime.now())
            hora, ponto, ms = lista.split()[1].partition('.')
            lista_hours.append(hora)
        x = [-2.5, 0.4, 4.2, 6.9, 7.8, 8, 10, 15, 25]
        y = [q**2-q+3 for q in x]
        trace1 = go.Scatter(x=lista_hours, y=lista_prices, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                            mode="lines",  name='1st Trace')
        data=go.Data([trace1])
        layout=go.Layout(title="Coffee Price", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        return context
    template_name = 'cafe.html'

class IndexView(TemplateView):

    template_name = 'index.html'


class ContatoView(TemplateView):

    template_name = 'contato.html'


class ComecandoView(TemplateView):

    template_name = 'comecando.html'


class SobreView(TemplateView):

    template_name = 'sobre.html'


class CriarContaView(TemplateView):

    template_name = 'criar-conta.html'


class CanalView(TemplateView):

    template_name = 'meu-canal.html'
index = IndexView.as_view()
contato = ContatoView.as_view()
comecando = ComecandoView.as_view()
sobre = SobreView.as_view()
criar_conta = CriarContaView.as_view()
canal = CanalView.as_view()
cafe = CafeView.as_view()
