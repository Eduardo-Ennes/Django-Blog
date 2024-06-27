from django.core.exceptions import ValidationError

def validators_image(image):
    if not image.name.lower().endswith('.png'):
        raise ValidationError('A imagem precisa ser PNG!')
    '''
    Essa função serve para validar a imagem enviada pelo usuário, que deverá aceitar apenas PNG
    '''