from site_setup.models import SiteSetup


def context_processors_setup(request):
    '''
    está view esta no context_processors no settings para tonar as varáveis dessa view globais e poder ser aplicavéis em todos os templates do projeto.
    '''
    setup = SiteSetup.objects.order_by('-id').first()
    # acessou o banco de dados SiteSetup ordenando de forma decrescente e pegando o primeiro valor do banco de dados
    
    return {
        'setup': setup
    }
