from .atividade import verificar_atividade

def verificar_dias(dias):
    if not dias:
        return False, "Falta a chave 'dias' no roteiro."

    for index, dia in enumerate(dias, start=1):
        dia_chave = next(iter(dia))
        if "data" not in dia[dia_chave]:
            return False, f"Falta a chave 'data' no Roteiro do dia_{index}."

        for periodo in ["manha", "tarde", "noite"]:
            if periodo in dia[dia_chave]:
                for atividade in dia[dia_chave][periodo]:
                    valido, msg = verificar_atividade(atividade)
                    if not valido:
                        return False, msg

    return True, ""