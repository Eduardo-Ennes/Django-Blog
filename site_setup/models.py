from django.db import models
from site_setup.utils.model_vlidators import validators_image
from site_setup.utils.image import resize_image


class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)
    
    url_or_path = models.CharField(max_length=2048)
    # Tambem poderiamos usar o Url_Field
    
    new_tab = models.BooleanField(default=False)
    # Essa opção será para abrir a página na mesma janela ou em outra janela. 
    
    site_setup = models.ForeignKey('SiteSetup', on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='menu')
    

    def __str__(self):
        return self.text



class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    '''
    Os shows são as opções se o usuário vai ou não querer mostrar as opções 
    '''
    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)
    
    favicon = models.ImageField(upload_to='assests/favicon/%y/%m/', blank=True, default='', 
                               validators=[validators_image] )
    '''
    validators=[validators_image] -> é uma função que valida a imagem enviada pelo usuário, que deverá ser apenas PNG
    '''
    
    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        if favicon_changed:
            '''
            resize_image -> é um metodo para redimencionar imagens que esta no arquivo utils/image.py 
            
            é apenas uma função que esta sendo chamada
            '''
            resize_image(self.favicon, 32)
        
    def __str__(self):
        return self.title