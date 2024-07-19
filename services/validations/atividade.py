from .common import verificar_chaves, verificar_float, verificar_moeda


def verificar_atividade(atividade):
    chaves_necessarias = [
        "atividade",
        "local",
        "latitude",
        "longitude",
        "horario",
        "custo_aproximado",
    ]
    valido, msg = verificar_chaves(atividade, chaves_necessarias, "atividade")
    if not valido:
        return False, msg

    for chave in ["latitude", "longitude"]:
        valido, msg = verificar_float(atividade[chave], chave)
        if not valido:
            return False, msg

    return verificar_moeda(atividade["custo_aproximado"], "custo_aproximado")
