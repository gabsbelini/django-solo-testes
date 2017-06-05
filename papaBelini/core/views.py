import urllib.request
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


class CafeView(TemplateView):
    def get_context_data(self, **kwargs):
        class AppURLopener(urllib.request.FancyURLopener):
            version = "Mozilla/5.0"
        opener = AppURLopener()
        response = opener.open('https://www.investing.com/commodities/us-coffee-c-contracts').read()
        soup = BeautifulSoup(response, 'html.parser')
        price = soup.find("td", {"class": "pid-8832-last"}).get_text()
        context = super(CafeView, self).get_context_data(**kwargs)
        context['preco'] = price
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
