from .common import verificar_chaves, verificar_moeda

def verificar_orcamento(orcamento):
    chaves_necessarias = ["media_das_hospedagens", "alimentacao", "ingressos", "transporte", "extras_compras", "total"]
    valido, msg = verificar_chaves(orcamento, chaves_necessarias, "orcamento")
    if not valido:
        return False, msg
    
    for chave in chaves_necessarias:
        valido, msg = verificar_moeda(orcamento[chave], chave)
        if not valido:
            return False, msg

    return True, ""
