def verificar_chaves(dic, chaves_necessarias, nome_objeto):
    for chave in chaves_necessarias:
        if chave not in dic:
            return False, f"Falta a chave {chave} em {nome_objeto}."
    return True, ""


def verificar_float(valor, nome_chave):
    try:
        float(valor)
    except ValueError:
        return False, f"{nome_chave} deve ser um número."
    return True, ""


def verificar_moeda(valor, nome_chave):
    partes = valor.split(" ")
    if len(partes) != 2 or not partes[1].replace(".", "", 1).isdigit():
        return (
            False,
            f"{nome_chave} deve estar no formato 'simbolo_moeda valor_em_número'.",
        )
    return True, ""
