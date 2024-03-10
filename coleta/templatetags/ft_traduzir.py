from django import template
from coleta.traducoes import traduzir

register = template.Library()

@register.simple_tag
def ft_traduzir(frase):
  return traduzir(frase)