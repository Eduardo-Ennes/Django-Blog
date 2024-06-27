'''
Neste projeto as views estavam sendo desenvolvidas com funções, no final do projeto vamos substituir funções para classes na view. Neste arquivo vou deixar salvo tadas as funções desenvolvidas do projeto, todas estão comentadas sobre o seu funcionamento e propósito no código.
'''

# IMPORTAÇÕES 
# from django.core.paginator import Paginator 
# from django.shortcuts import render
# from project.models import Post, Page
# from django.db.models import Q
# from django.contrib.auth.models import User
# from django.http import Http404




# INDEX
# def Index(request):
#     posts = Post.objects.get_published()
#     '''
#     Este metodo foi criado para não termos que escrever o código padrão de busca aqui na view, ele está no banco de dados, duvida consultar o 
    
#     esse metodo está interligado no model Post e admin Post
    
#     para melhor entendimento consultar aonde está interligado 
#     '''
    
#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     '''
#     Codigo paginator 
#     '''
#     context = {
#         'page_obj': page_obj,
#         'page_title': 'Home'
#     }
#     return render(request, 'index.html', context)





# AUTHOR 
# def Author(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()
#     if user is None:
#         raise Http404()
    
#     user_full_name = user.username
#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
#     page_title = 'Posts de ' + user_full_name + ' - '
#     '''
#     Este campo serve para buscar o nome do usuário e colocar na titulo de pesquisa.
#     '''
    
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk) 
#     '''
#     Essa view está linkada no post.html na parte do Author name, ela está redirecionando para uma pagina que mostrará apenas publicações do propio autor.
#     '''
#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'page_obj': page_obj,
#         'page_title': page_title
#     }
#     return render(request, 'index.html', context)





# CATEGORIA
# def Categoria(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug) 
#     '''
#     Essa view está linkada no post.html na parte do Category, ela está redirecionando para uma pagina que mostrará todas as publicações relacionadas a essa categoria.
#     '''
#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     if len(page_obj) == 0:
#         raise Http404
    
#     page_title = f'{page_obj[0].category.name} - Categoria - '
    
#     context = {
#         'page_obj': page_obj,
#         'page_title': page_title
#     }
#     return render(request, 'index.html', context)




# Tag
# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug) 
#     '''
#     Essa view busca no banco de dados do Post o valor tags que é um foreingkey do banco de dados Tag, no valor tags contem todo um banco de dados por ser uma foreingkey. 
    
#     Quando clicarmos em uma tag no publicação irá mostrar apenas publicações relacionadas a tag selecionada. 
    
#     Essa view funciona da mesma forma que a view categoria logo acima. Ambas estão buscando valores de uma foreignkey. Já na view Author a forma de se buscar o valor é similar, porem não é de uma foreignkey. 
    
#     Algumas views neste projeto tabalham de forma similar ou iguais, nesta view em especifico as explicações são um pouco mais claras e leva a um melhor entendimento de como elas funcionam ou para um consulta    
#     '''
#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     if len(page_obj) == 0:
#         raise Http404
    
#     page_title = f'{page_obj[0].tags.first().name} - '
    
#     context = {
#         'page_obj': page_obj,
#         'page_title': page_title
#     }
#     return render(request, 'index.html', context)





# Search
# def Search(request):
#     '''
#     Deve-se importar a biblioteca Q para filtrar os valores da busca.
    
#     Este é um exemplo que deu certo para busca de valores no post. Seguir este exemplo.
    
#     consultar também o template e url que contém para a busca do search
#     '''
#     search_value = request.GET.get('Search', '').strip()
#     posts = (
#         Post.objects.get_published()
#              .filter(
#                  Q(title__icontains=search_value) |
#                  Q(excerpt__icontains=search_value) |
#                  Q(content__icontains=search_value)
#                      ))[:9]
    
#     page_title = f'{search_value[:30]} - Search - '
    
#     context = {
#         'page_obj': posts,
#         'search_value': search_value,
#         'page_title': page_title
#     }
#     return render(request, 'index.html', context)





# Publicação
# def Publicacao(request, slug):
#     page = Page.objects.filter(is_published=True).filter(slug=slug).first()
    
#     # paginator = Paginator(posts, 9)
#     # page_number = request.GET.get("page")
#     # page_obj = paginator.get_page(page_number)
    
#     if page is None:
#         raise Http404
    
#     page_title = f'{page.title} - página - '
    
#     context = {
#         'page': page,
#         'page_title': page_title
#     }

#     return render(request, 'page.html', context)





# Paginas 
# def Paginas(request, slug):
#     post = Post.objects.get_published().filter(slug=slug).first()    
 
#     if post is None:
#         raise Http404
    
#     page_title = f'{post.title} - post - '
 
#     return render(request, 'post.html',
#         {
#             'post': post,
#             'page_title': page_title
#         })