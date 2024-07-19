from .validations.common import verificar_chaves
from .validations.hospedagem import verificar_recomendacoes_hospedagem
from .validations.orcamento import verificar_orcamento
from .validations.dias import verificar_dias


def verificar_json(json_data):
    if "roteiro" not in json_data:
        return False, "Falta a chave 'roteiro' no JSON."

    roteiro = json_data["roteiro"]
    chaves_necessarias = ["recomendacoes_hospedagem", "orcamento", "dicas_observacoes"]
    valido, msg = verificar_chaves(roteiro, chaves_necessarias, "roteiro")
    if not valido:
        return False, msg

    valido, msg = verificar_dias(roteiro.get("dias"))
    if not valido:
        return False, msg

    valido, msg = verificar_recomendacoes_hospedagem(
        roteiro["recomendacoes_hospedagem"]
    )
    if not valido:
        return False, msg

    valido, msg = verificar_orcamento(roteiro["orcamento"])
    if not valido:
        return False, msg

    if not all(chave.isdigit() for chave in roteiro["dicas_observacoes"]):
        return False, "As chaves em 'dicas_observacoes' devem ser números sequenciais."

    return True, "JSON válido."
