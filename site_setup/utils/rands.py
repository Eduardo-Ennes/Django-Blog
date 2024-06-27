import string
from random import SystemRandom
from django.utils.text import slugify

def random_tetters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_letters + string.digits, k=k
    ))
    
    
def slugfy_new(text):
    return slugify(text) + random_tetters()     
    
    
# Esta é uma função que gera um código para o slug caso o usuário não o preencha, ai terá este valor gerado.