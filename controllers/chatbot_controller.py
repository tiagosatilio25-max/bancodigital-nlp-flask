from flask import Blueprint, render_template, request
from models.database import salvar_mensagem, obter_historico_df
from services.nlp_service import identificar_intencao

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        texto = request.form.get('texto', '')
        if texto.strip():
            intencao, lemmas = identificar_intencao(texto)
            salvar_mensagem(texto, intencao, lemmas)
            resultado = {
                'texto': texto,
                'intencao': intencao,
                'lemmas': lemmas
            }
            
    df_historico = obter_historico_df()
    historico = df_historico.to_dict(orient='records')
    
    return render_template('index.html', resultado=resultado, historico=historico)