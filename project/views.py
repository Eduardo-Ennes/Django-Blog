from typing import Any 
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from project.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView



'''
Ordem dos metodos:
1 - setup()
2 - dispatch()
3 - http_method_not_allowed()
4 - get_template_names()
5 - get_queryset()
6 - get_context_object_name()
7 - get_context_data()
8 - get()
9 - render_to_responde()
'''



PER_PAGE = 9



class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context.update({
            'page_title': 'Home - ',
        })
        
        return context



class AuthorListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)



class CategoryListView(PostListView):
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (f'{self.object_list[0].category.name} - categoria - ')
        ctx.update({
            'page_title': page_title,
        })
        return ctx



class TagListView(PostListView):
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (f'{self.object_list[0].tags.first().name} - Tag - ')
        ctx.update({
            'page_title': page_title,
        })
        return ctx



class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''
        
    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('Search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
            )[:PER_PAGE]
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value
        })
        return ctx
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('Index')
        return super().get(request, *args, **kwargs)



class PublicacaoDetailView(DetailView):
    model = Page
    template_name = 'page.html'
    slug_field = 'slug'
    context_object_name = 'page'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - página - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    
    
   
class PaginasDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - Post - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)