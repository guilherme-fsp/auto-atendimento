from flask import Blueprint, render_template, request
from dados_conversa import dias, contagens, usuarios_unicos, cidades_diferentes, conversas_por_numero

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route("/")
def home_page():
    return render_template("home.html")

@frontend_bp.route("/historico")
def historico():
    return render_template("historico.html", conversas_por_numero=conversas_por_numero)

@frontend_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.jinja",
    dias=["Seg", "Ter", "Qua", "Qui", "Sex"],
    contagens=[12, 9, 15, 7, 11],
    total_mensagens=sum(contagens),
    usuarios_unicos=5,
    cidades_diferentes=3)


@frontend_bp.route("/conversas")
def pagina_conversas():
    return render_template("conversas.html")

     #return render_template("dashboard.html",
                         #  dias=dias,
                          # contagens=contagens,
                           #total_mensagens=sum(contagens),
                          # usuarios_unicos=usuarios_unicos,
                           #cidades_diferentes=cidades_diferentes)
