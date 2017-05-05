from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


class IndexView(TemplateView):

    template_name = 'index.html'


index = IndexView.as_view()
