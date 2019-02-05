from django.shortcuts import render, HttpResponse, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Object, Types, Typ, Rayon, News
from django.views.generic.list import ListView
from django.views.generic import DetailView
import random


def index(request):
    #object_list = Object.objects.all()

    #paginator = Paginator(object_list, 1)
    #page = request.GET.get('page')
    #try:
    #    posts = paginator.page(page)
    #except PageNotAnInteger:
    #    posts = paginator.page(1)
    #except EmptyPage:
    #    posts = paginator.page(paginator.num_pages)

    types_list = Types.objects.all()
    typs_list = Typ.objects.all()
    ray_list = Rayon.objects.all()
    news_list = News.objects.all().order_by('?')[:2]

    random_objects = Object.objects.all().order_by('?')[:6]
    return render(
        request,
        'index.html',
        {
            'types': types_list,
            'typs': typs_list,
            'ray': ray_list,
            'news': news_list,
            'random': random_objects,
        },
    )


class Robject(DetailView):
    queryset = Object.objects.all()
    template_name = "object.html"

    def get_object(self, queryset=None):
        obj = None
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get("pk"))
        print(queryset)
        try:
            obj = queryset.get()
        except Exception:
            print(queryset.model._meta.verbose_name)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rez = Object.objects.filter(komnat=self.object.komnat)
        news_list = News.objects.all().order_by('?')[:2]
        rez = rez.exclude(id=self.object.id)
        #number_of_records = rez.objects.count()
        #k = [random.choice(rez) for k in range(3)]
        context['rez'] = rez.order_by('?')[:3]
        context['news'] = news_list
        return context


class Nobject(DetailView):
    queryset = News.objects.all()
    template_name = "news.html"

    def get_object(self, queryset=None):
        obj = None
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get("pk"))
        try:
            obj = queryset.get()
        except Exception:
            print(queryset.model._meta.verbose_name)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('?')[:2]
        return context


def objects(request, pk):
    return render_to_response("objects.html")


def about(request):
    return render_to_response("about.html",{'news': News.objects.all().order_by('?')[:2]})


class AllObjects(ListView):
    model = Object
    paginate_by = 21
    template_name = 'objects.html'
    context_object_name = 'objects'
    type = typ = ray = cost = s = 0
    v1 = s1 = 0
    v2 = 25000000
    s2 = 250

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['types_list'] = Types.objects.all()
        context['typs_list'] = Typ.objects.all()
        context['ray_list'] = Rayon.objects.all()
        context['news'] = News.objects.all().order_by('?')[:2]
        context['search_params'] = (self.type, self.typ, self.ray, self.cost, self.s,)
        return context

    def get_queryset(self):
        k = Object.objects.all().order_by("?")
        if self.request.GET.get('p1'):
            self.type = int(self.request.GET.get('p1'))
        if self.request.GET.get('p2'):
            self.typ = int(self.request.GET.get('p2'))
        if self.request.GET.get('p3'):
            self.ray = int(self.request.GET.get('p3'))
        if self.request.GET.get('p4'):
            self.cost = self.request.GET.get('p4')
            if self.cost != '0' and self.cost != 0:
                self.v1, self.v2 = self.cost.split(',')
        if self.request.GET.get('p5'):
            self.s = self.request.GET.get('p5')
            if self.s != 0 and self.s != '0':
                self.s1, self.s2 = self.s.split(',')

        if self.type != 0: k = k.filter(type__id=self.type)
        if self.typ != 0: k = k.filter(typ__id=self.typ)
        if self.ray != 0: k = k.filter(rayon__id=self.ray)
        if int(self.v1) != 0 or int(self.v2) != 25000000: k = k.filter(cost__gte=int(self.v1), cost__lte=int(self.v2))
        if int(self.s1) != 0 or int(self.s2) != 250: k = k.filter(s__gte=int(self.s1), s__lte=int(self.s2))
        return k
