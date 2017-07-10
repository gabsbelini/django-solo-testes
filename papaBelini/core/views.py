import urllib.request
from bs4 import BeautifulSoup
from .models import Commodity
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import quandl
import requests
import json
import numpy as np

from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .forms import GraphForm
from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
import plotly.offline as opy
import plotly.graph_objs as go


url_coffe_futures = 'https://www.quandl.com/api/v3/datasets/CHRIS/ICE_KC1'
rjson = requests.get(url_coffe_futures).json()

lista_caiu = [0, 0, 0, 0, 0]
lista_subiu = [0, 0, 0, 0, 0]
subiu = 0
caiu = 0
indice = 3
for dia in range(5):
    for variacao in np.arange(dia, 200, 5):
        if (rjson['dataset']['data'][variacao][5] != None and rjson['dataset']['data'][variacao][5] > 0.0):
            subiu += 1
        elif (rjson['dataset']['data'][variacao][5] != None and rjson['dataset']['data'][variacao][5] < 0.0):
            caiu += 1
    print('inseriu no indice', indice)
    lista_subiu[indice] = subiu
    lista_caiu[indice] = caiu
    subiu = 0
    caiu = 0
    if indice == 0:
        indice = 4
    else:
        indice -= 1
class CafeView(TemplateView):
    #Commodity.objects.all().delete()
    def get_context_data(self, **kwargs):
        class AppURLopener(urllib.request.FancyURLopener):
            version = "Mozilla/5.0"
        opener = AppURLopener()
        response = opener.open('https://www.investing.com/commodities/us-coffee-c-contracts').read()
        soup = BeautifulSoup(response, 'html.parser')
        price = float(soup.find("td", {"class": "pid-8832-last"}).get_text())
        price_var_points = float(soup.find("td", {"class": "pid-8832-pc"}).get_text())
        context = super(CafeView, self).get_context_data(**kwargs)
        context['preco'] = price
        context['tiponow'] = type(datetime.datetime.now().time())
        context['timenow'] = datetime.datetime.now().time()
        datetime_banco = Commodity.objects.latest('id').time
        datetime_padrao = datetime.datetime.now()
        print((datetime_banco), (datetime_padrao))
        if price_var_points >= 0.0:
            cafe = Commodity(name='cafe', price=price, variation='+'+str(price_var_points))
            context['pontos_positivo'] = str(price_var_points)
        else:
            cafe = Commodity(name='cafe', price=price, variation='-'+str(price_var_points))
            context['pontos_negativo'] = str(price_var_points)
        context['commodity_time'] = cafe.time

        cafe.save()
        context['tipo_commodity_time'] = type(cafe.time)
        y = [obj.price for obj in Commodity.objects.all()]
        x = [obj.time for obj in Commodity.objects.all()]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                            mode="lines",  name='1st Trace')
        data=go.Data([trace1])
        layout=go.Layout(title="Coffee Price", xaxis={'title':'Hora'}, yaxis={'title':'Preço U$'})
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
    form_class = GraphForm
    def get_context_data(self, **kwargs):
        context = super(ComecandoView, self).get_context_data(**kwargs)
        lista_precos = []
        lista_datas = []
        for variacao in range(10500):
            lista_precos.append(rjson['dataset']['data'][variacao][4])
            lista_datas.append(rjson['dataset']['data'][variacao][0])

        # Create a trace
        trace = go.Scatter(
            y = lista_precos,
            x = lista_datas
        )

        data = [trace]
        fig = go.Figure(data=data)
        div = opy.plot(fig, auto_open=False, output_type='div')
        context['graph'] = div
        return context
    def form_valid(self, form):
        form.send_email()
        return super(ComecandoView, self).form_valid(form)
    template_name = 'comecando.html'


class SobreView(TemplateView):
    #Commodity.objects.all().delete()
    def get_context_data(self, **kwargs):
        context = super(SobreView, self).get_context_data(**kwargs)
        trace1 = go.Bar(
        x=['segunda', 'terca', 'quarta', 'quinta', 'sexta'],
            y=lista_subiu,
            name='Subiu'
        )
        trace2 = go.Bar(x=['segunda', 'terca', 'quarta', 'quinta', 'sexta'],
            y=lista_caiu,
            name='Caiu')
        data = [trace1, trace2]
        layout = go.Layout(
            barmode='group'
        )
        fig = go.Figure(data=data, layout=layout)
        div = opy.plot(fig, auto_open=False, output_type='div')
        context['graph'] = div
        return context
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
