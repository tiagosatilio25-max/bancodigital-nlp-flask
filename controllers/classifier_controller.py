from flask import Blueprint, render_template, request
from models.database import salvar_solicitacao, obter_historico_df
from services.nlp_service import classificar_texto

classifier_bp = Blueprint('classifier', __name__)

@classifier_bp.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        texto = request.form.get('texto', '')
        if texto.strip():
            categoria, lemmas = classificar_texto(texto)
            salvar_solicitacao(texto, categoria, lemmas)
            resultado = {
                'texto': texto,
                'categoria': categoria,
                'lemmas': lemmas
            }
            
    # Obtém o histórico com fallback seguro em caso de indisponibilidade da rede/banco
    df_historico = obter_historico_df()
    historico = df_historico.to_dict(orient='records')
    
    return render_template('index.html', resultado=resultado, historico=historico)