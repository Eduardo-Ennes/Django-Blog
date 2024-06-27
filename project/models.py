from django.db import models
from site_setup.utils.rands import slugfy_new
from site_setup.utils.image import resize_image
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment
from django.urls import reverse




class PostAttachment(AbstractAttachment):
    '''
    Aqui criamos o model para o summernote, automaticamente substitui o model que vem por padrão. Em seguida sobrescrevemos o metodo save para redimencionar as imagens que serão carregadas no summenote.
    '''
    def save(self, *args, **kwargs):
        
        if not self.name:
            self.name = self.file.name
            
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            '''
            resize_image -> é um metodo para redimencionar imagens que esta no arquivo utils/image.py 
            
            é apenas uma função que esta sendo chamada para redimencionar as imagens 
            '''
            resize_image(self.file, 900, True, 70)
            
        return super_save




class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, default=None, blank=True, null=True, max_length=150)
    
    def save(self, *args, **kwargs):
        '''
        Este metodo está interligado está interligado com o rands.py para criação do slugfy para colocar na url.
        '''
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
    
    
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, default=None, blank=True, null=True, max_length=150)
    
    def save(self, *args, **kwargs):
        '''
        Este metodo está interligado está interligado com o rands.py para criação do slugfy para colocar na url.
        '''
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
    
    
    
class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, default=None, blank=True, null=True, max_length=150)
    is_published = models.BooleanField(default=False, help_text=('Este campo precisa estar marcado para que a página possa ser exibida publicamente.'))
    content = models.TextField()
    
    def get_absolute_url(self):
        '''
        esse metodo está interligado na admin post e view index
        
        para melhor entendimento consultar aonde está interligado 
        '''
        if not self.is_published:
            return reverse('Index')
        return reverse('Publicacao', args=(self.slug,))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
     
     
     
     
class PostManager(models.Manager):
    '''
    Este é um metodo para não termos que fazer a mesma busca na views, duvida ir na view Index
    '''
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')     
    
    
    
    
    
    
# Aqui começa o banco de dados Post, maior e mais complexo        
class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    objects = PostManager()
    # este metodo linka a classe PostManager a este banco de dados, que serviu para fazer a busca na view index
        
    title = models.CharField(max_length=150)
    
    slug = models.SlugField(unique=True, default=None, blank=True, null=True, max_length=150)
    
    excerpt = models.CharField(max_length=150)
    
    content = models.TextField()
    '''
    content é a parte que contém o summernote e o conteúdo da publicação do usuário, temos configuração code_mirror no _head.html e _footer.html
    
    
    configuração muito importante!!
    configuração dentro do summernote para o code_mirror: 
    - <pre data-language="python"> colocar todo o conteudo desejado dentro da tag </pre>
    '''
    
    is_published = models.BooleanField(default=False, help_text=('Este campo precisa estar marcado para que a página possa ser exibida publicamente.'))
    # Habilita se publica ou não
    
    cover = models.ImageField(upload_to='post/%y/%m', blank=True, default='')
    # cover funciona para anexar imagens, as imagens estão sendo redimencionadas na função save la embaixo. upload_to='post/%y/%m' as imagens estão sendo colocadas nesta pagina 
    
    cover_in_post_content = models.BooleanField(default=True, help_text='se marcado, exibirá a capa dentro do post.')
    # serve para habilitar caso o usuário queira ou não mostrar a imagem.
    
    created_at = models.DateTimeField(auto_now_add=True)
    # mostra a data de criação apenas 
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='page_created_by')
    # mostra o usuário que adicionou um novo elemento
    
    updated_at = models.DateField(auto_now=True)
    # mostra a data de atualização
    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='page_updated_by')
    # mostra o usuário que atualizou
    # não é muito usado

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    
    tags = models.ManyToManyField(Tag, blank=True, default='')
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        '''
        esse metodo está interligado na admin post e view index
        
        para melhor entendimento consultar aonde está interligado 
        '''
        if not self.is_published:
            return reverse('Index')
        return reverse('Paginas', args=(self.slug,))
    
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugfy_new(self.title, 4)
    
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            '''
            resize_image -> é um metodo para redimencionar imagens que esta no arquivo utils/image.py 
            
            é apenas uma função que esta sendo chamada
            '''
            resize_image(self.cover, 900, True, 70)
            
        return super_save
    