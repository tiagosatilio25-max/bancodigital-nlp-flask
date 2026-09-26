import spacy

nlp = spacy.load("pt_core_news_sm")

# Dicionário de Intenções baseado em Lemas (formas base das palavras)
REGRAS_INTENCOES = {
    "Cancelar": {
        "cancelar", "cancelamento", "desistir", "estorno", "devolver", 
        "encerrar", "anular", "descontinuar"
    },
    "Comprar": {
        "comprar", "compra", "adquirir", "contratar", "preco", "valor", 
        "desconto", "plano", "assinar", "carrinho"
    },
    "Suporte": {
        "suporte", "ajuda", "problema", "erro", "defeito", "falar", 
        "atendimento", "duvida", "tecnico", "manual", "funcionar"
    }
}

def identificar_intencao(texto):
    doc = nlp(texto.lower())
    
    # Extrai lemas (lemmatization) ignorando pontuações e stop words
    lemmas = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    set_lemmas = set(lemmas)
    
    pontuacoes = {}
    for intencao, palavras_chave in REGRAS_INTENCOES.items():
        # Conta interseções entre lemas da mensagem e palavras da regra
        intersecao = set_lemmas.intersection(palavras_chave)
        pontuacoes[intencao] = len(intersecao)
    
    # Pega a intenção com maior pontuação
    intencao_detectada = max(pontuacoes, key=pontuacoes.get)
    
    # Se não houver correspondência de palavras-chave
    if pontuacoes[intencao_detectada] == 0:
        intencao_detectada = "Não Identificada / Outros"
        
    return intencao_detectada, lemmas