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


from django.shortcuts import HttpResponse
from django.core.exceptions import *
from django.http import HttpResponseRedirect
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
        context = super(CafeView, self).get_context_data(**kwargs)
                # Create trace lists
        lista_precos_max = []
        lista_datas_max = []
        for variacao in range(len(rjson['dataset']['data'])):
            lista_precos_max.append(rjson['dataset']['data'][variacao][4])
            lista_datas_max.append(rjson['dataset']['data'][variacao][0])

        lista_precos_semestre = []
        lista_datas_semestre = []
        for variacao in range(132):
            lista_precos_semestre.append(rjson['dataset']['data'][variacao][4])
            lista_datas_semestre.append(rjson['dataset']['data'][variacao][0])


        lista_precos_mes = []
        lista_datas_mes = []
        for variacao in range(23):
            lista_precos_mes.append(rjson['dataset']['data'][variacao][4])
            lista_datas_mes.append(rjson['dataset']['data'][variacao][0])

        lista_precos_semana = []
        lista_datas_semana = []
        for variacao in range(5):
            lista_precos_semana.append(rjson['dataset']['data'][variacao][4])
            lista_datas_semana.append(rjson['dataset']['data'][variacao][0])

        # Create traces
        trace_max = go.Scatter(
            y = lista_precos_max,
            x = lista_datas_max,
            fill='tonexty',
            line=go.Line(color='blue')
        )
        trace_semestre = go.Scatter(
            y = lista_precos_semestre,
            x = lista_datas_semestre,
            visible = False,
            fill='tonexty',
            line=go.Line(color='orange')

        )
        trace_mes = go.Scatter(
            y = lista_precos_mes,
            x = lista_datas_mes,
            fill='tonexty',
            visible = False,
        )
        trace_semana = go.Scatter(
            y = lista_precos_semana,
            x = lista_datas_semana,
            fill='tonexty',
            visible = False,
        )
        layout = go.Layout(
            title="Cotação do Café em Dólares Americanos (U$)",
            xaxis=dict(
                title="Período",
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title="Valor U$",
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                rangemode="normal"
            ),
            updatemenus=list([
                dict(
                    buttons=list([
                        dict(
                            args=['visible', [True, False, False, False]],
                            label='Variação Anual',
                            method='restyle'
                        ),
                        dict(
                            args=['visible', [False, True, False, False]],
                            label='Variação Semestral',
                            method='restyle'
                        ),
                        dict(
                            args=['visible', [False, False, True, False]],
                            label='Variação Mensal',
                            method='restyle'
                        ),
                        dict(
                            args=['visible', [False, False, False, True]],
                            label='Variação Semanal',
                            method='restyle'
                        )
                    ]),
                )
            ]),
        )


        data = go.Data([trace_max, trace_semestre, trace_mes, trace_semana])
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
    def post(self, request, *args, **kwargs):
        dado = request.POST["textfield"]
        context = super(SobreView, self).get_context_data(**kwargs)
        context['dado'] = dado
        return HttpResponseRedirect('sobre')

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
