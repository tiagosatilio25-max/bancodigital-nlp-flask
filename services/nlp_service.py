import spacy

nlp = spacy.load("pt_core_news_sm")

INTENCOES = {
    "Bloqueio de Cartão": {"bloquear", "cartao", "perda", "roubo", "furtado", "cancelar", "bloqueio"},
    "Segunda Via de Boleto": {"boleto", "segunda", "via", "fatura", "codigo", "barras", "vencimento", "pagar"},
    "Consulta de Saldo/Extrato": {"saldo", "extrato", "conta", "dinheiro", "sobra", "consultar", "quanto"},
    "Suporte Geral": {"atendimento", "falar", "humano", "ajuda", "suporte", "duvida"}
}

def classificar_texto(texto):
    doc = nlp(texto.lower())
    
    lemmas = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    set_lemmas = set(lemmas)
    
    pontuacoes = {}
    for intencao, palavras_chave in INTENCOES.items():
        intersecao = set_lemmas.intersection(palavras_chave)
        pontuacoes[intencao] = len(intersecao)
    
    categoria = max(pontuacoes, key=pontuacoes.get)
    if pontuacoes[categoria] == 0:
        categoria = "Não Identificado"
        
    return categoria, lemmas