def verificar_json(json_data):

    def verificar_atividade(atividade):
        required_keys = ["atividade", "local", "latitude", "longitude", "horario", "custo_aproximado"]
        for key in required_keys:
            if key not in atividade:
                return False, f"Falta a chave {key} na atividade."
            if key in ["latitude", "longitude"]:
                try:
                    float(atividade[key])
                except ValueError:
                    return False, f"{key} deve ser um número."
            if key == "custo_aproximado":
                partes = atividade[key].split(" ")
                if len(partes) != 2 or not partes[1].replace('.', '', 1).isdigit():
                    return False, f"custo_aproximado deve estar no formato 'simbolo_moeda valor_em_número'."
        return True, ""
        
    def verificar_hospedagem(hospedagem):
        required_keys = ["nome", "localizacao", "latitude", "longitude", "preco_medio", "comodidades"]
        for key in required_keys:
            if key not in hospedagem:
                return False, f"Falta a chave {key} na hospedagem."
            if key in ["latitude", "longitude"]:
                try:
                    float(hospedagem[key])
                except ValueError:
                    return False, f"{key} deve ser um número."
            if key == "preco_medio":
                partes = hospedagem[key].split(" ")
                if len(partes) != 2 or not partes[1].replace('.', '', 1).isdigit():
                    return False, f"Preço Médio deve estar no formato 'simbolo_moeda valor_em_número'."
        return True, ""    
    
    def verificar_orcamento(orcamento):
        required_keys = ["media_das_hospedagens", "alimentacao", "ingressos", "transporte", "extras_compras", "total"]
        for key in required_keys:
            if key not in orcamento:
                return False, f"Falta a chave {key} no orçamento."
            partes = orcamento[key].split(" ")
            if len(partes) != 2 or not partes[1].replace('.', '', 1).isdigit():
                return False, f"{key} deve estar no formato 'simbolo_moeda valor_em_número'."
        return True, ""
    
    if "roteiro" not in json_data:
        return False, "Falta a chave 'roteiro' no JSON."
    
    required_keys = ["recomendacoes_hospedagem", "orcamento", "dicas_observacoes"]

    for key in required_keys:
        if key not in json_data["roteiro"]:
            return False, f"Falta a chave '{key}' no JSON."

    if "dias" not in json_data["roteiro"]:
        return False, "Falta a chave 'dias' no roteiro."
    
    for index, dia in enumerate(json_data["roteiro"]["dias"], start=1):
        if "data" not in dia[next(iter(dia))]:
            dia_numero = f"dia_{index}"
            return False, f"Falta a chave 'data' no Roteiro do {dia_numero}."

        for periodo in ["manha", "tarde", "noite"]:
            if periodo in dia[next(iter(dia))]:
                for atividade in dia[next(iter(dia))][periodo]:
                    valido, msg = verificar_atividade(atividade)
                    if not valido:
                        return False, msg
    
    for hospedagem in json_data["roteiro"]["recomendacoes_hospedagem"]:
        valido, msg = verificar_hospedagem(hospedagem)
        if not valido:
            return False, msg
        
    valido, msg = verificar_orcamento(json_data["roteiro"]["orcamento"])
    if not valido:
        return False, msg
    
    if not all(key.isdigit() for key in json_data["roteiro"]["dicas_observacoes"]):
        return False, "As chaves em 'dicas_observacoes' devem ser números sequenciais."
    
    return True, "JSON válido."
