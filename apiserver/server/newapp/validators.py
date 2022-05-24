import magic
from django.core.exceptions import ValidationError

#Validação de imagens, tamanho máximo permitido: 20MB
def valida_img(file):
    tipo_ficheiro = magic.from_buffer(file.read(1024), mime=True)
    tamanho_ficheiro = file.size
    if "image" in tipo_ficheiro and tamanho_ficheiro<20971520:
        return True
    else:
        raise ValidationError('Falha ao submeter ficheiro. Certifique-se que é uma imagem e que não alcança os 20MB.')

#Vlidação de videos, tamanho máximo permitido: 500MB
def valida_video(file):
    tipo_ficheiro = magic.from_buffer(file.read(1024), mime=True)
    tamanho_ficheiro = file.size
    if "video" in tipo_ficheiro and tamanho_ficheiro<429916160:
        return True
    else:
        raise ValidationError('Falha ao submeter ficheiro. Certifique-se que é um video e que não alcança os 500MB.')

#Validação de pdf, tamanho máximo permitido: 5MB
def valida_pdf(file):
    tipo_ficheiro = magic.from_buffer(file.read(1024), mime=True)
    tamanho_ficheiro = file.size
    print(file.size)
    if "pdf" in tipo_ficheiro and tamanho_ficheiro<5242880:
        return True
    else:
        raise ValidationError('Falha ao submeter ficheiro. Certifique-se que é um pdf e que não alcança os 5MB.')
