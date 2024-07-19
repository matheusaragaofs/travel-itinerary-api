from .common import verificar_chaves, verificar_float, verificar_moeda

def verificar_hospedagem(hospedagem):
    chaves_necessarias = ["nome", "localizacao", "latitude", "longitude", "preco_medio", "comodidades"]
    valido, msg = verificar_chaves(hospedagem, chaves_necessarias, "hospedagem")
    if not valido:
        return False, msg

    for chave in ["latitude", "longitude"]:
        valido, msg = verificar_float(hospedagem[chave], chave)
        if not valido:
            return False, msg

    return verificar_moeda(hospedagem["preco_medio"], "preco_medio")


def verificar_recomendacoes_hospedagem(recomendacoes_hospedagem):
    for hospedagem in recomendacoes_hospedagem:
        valido, msg = verificar_hospedagem(hospedagem)
        if not valido:
            return False, msg
    return True, ""