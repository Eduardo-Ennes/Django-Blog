from django.contrib import admin
from django.http import HttpRequest
from site_setup.models import MenuLink, SiteSetup

'''
@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = 'id', 'text', 'url_or_path',
    list_display_links = 'id', 'text', 'url_or_path',
    search_fields = 'id', 'text', 'url_or_path',
    # Busca personalizada 
    
    Não precisamos mais desse admin, logo abaixo foi criado um outro MenuLink que foi linkado no SiteSetup e ele será exibido e cotrolado diretamente no SiteSetup.
'''


'''
A classe MenuLinkInline está linkada a SiteSetupAdmin, a função abaixo é uma forma de mostramos os links no admin, como está linkado ao setup, será exibido no admin do setup.
'''

class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    '''
    Novo admin do MenuLink criado, e este foi linkado com o SiteSetup e será mostrado e preenchido diretamente do SiteSetup
    
    StackedInline -> faz a mesma função do que o tabularInline, muda apenas o estilo.
    '''  
    extra = 1   
    # Deixa apenas uma caixa de sobra para colocar as informações, vem 3 por padrão


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = MenuLinkInline,
    '''
    inlines = MenuLinkInline, --> É a forma de linkar os admins
    '''

    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()
        '''
        A função acima excuta: se no setup já houver dados desabilitará a opção de adcionar dados, podendo apenas ficar com um dado no setup
        '''