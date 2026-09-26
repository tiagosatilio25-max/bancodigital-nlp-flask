from flask import Flask
from controllers.classifier_controller import classifier_bp

app = Flask(__name__)

# Regista os blueprints / rotas
app.register_blueprint(classifier_bp)

# ESTA PARTE É A QUE FAZ O SERVIDOR ARRANCAR NO TERMINAL:
if __name__ == '__main__':
    app.run(debug=True)