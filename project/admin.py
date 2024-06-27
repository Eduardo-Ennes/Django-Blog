from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from project.models import Tag, Category, Page, Post
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    # mostra os campos no admin
    
    list_display_links = 'name',
    # Quais campos poderão servir como link para acessar o perfil
    
    search_fields = 'id', 'name', 'slug',
    # Por quais campos podeos fazer uma busca personalizada
    
    list_per_page = 10
    # quantos usuários irão aparecer por pagiana
    
    ordering = ['-id',]
    # Odenação da lista
    
    prepopulated_fields = {
        "slug": ('name',),
    }
    # faz com que o slug tenha o valor do banco de dados 
    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    # mostra os campos no admin
    
    list_display_links = 'name',
    # Quais campos poderão servir como link para acessar o perfil
    
    search_fields = 'id', 'name', 'slug',
    # Por quais campos podeos fazer uma busca personalizada
    
    list_per_page = 10
    # quantos usuários irão aparecer por pagiana
    
    ordering = ['-id',]
    # Odenação da lista
    
    prepopulated_fields = {
        "slug": ('name',),
    }
    # faz com que o slug tenha o valor do banco de dados 
    
    
    
@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    '''
    SummernoteModelAdmin -> Por que o page tem um campo de texto chamado content, o summernote personaliza a área de texto igual ao summernote mesmo
    '''
    list_display = 'id', 'title', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = ['-id',]
    prepopulated_fields = {
        "slug": ('title',),
    }



@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published',  'created_by',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'excerpt', 'content',
    list_per_page = 50
    list_filter = 'category', 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by', 'link'
    prepopulated_fields = {
        "slug": ('title',),
    }
    autocomplete_fields = 'tags', 'category',
    
    def link(self, obj):
        '''
        esse metodo está interligado no model Post e view index
        
        para melhor entendimento consultar aonde está interligado 
        '''
        if not obj.pk:
            return '-'
        url_do_post = obj.get_absolute_url()
        safe_link = mark_safe(
            f'<a target="_blank" href="{url_do_post}">Ver post</a>'
        )
        return safe_link
    
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()
        
        '''
        Aqui estamos sobrescervendo o metodo save, caso o usuário atualize os dados ativara o change e mostrará no admin o nome do usuário que atualizou os dados, seo usuário adicionar será ativado o else e também mostrará o usuário no admin que criou algo novo.
        
        Essa função é para que funcione o created_by e o updated_by.
        '''