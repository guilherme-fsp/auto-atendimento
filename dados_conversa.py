from registro_historico import carregar_conversas
from collections import defaultdict
from datetime import datetime

conversas = carregar_conversas()

# Agrupar por número
conversas_por_numero = defaultdict(list)
for c in conversas:
    conversas_por_numero[c["numero"]].append(c)

# Dados para o dashboard
contagem_por_dia = defaultdict(int)
cidades = set()
usuarios = set()

for c in conversas:
    try:
        # Converter data para datetime, ignorar mensagens sem data válida
        data_obj = datetime.strptime(c["data"], "%Y-%m-%d")
        dia = data_obj.strftime("%a")  # Nome do dia da semana
        contagem_por_dia[dia] += 1
        cidades.add(c.get("cidade", "Indefinida"))
        usuarios.add(c["numero"])
    except (KeyError, ValueError):
        continue

# Ordenar os dias da semana manualmente para manter ordem correta
ordem_dias = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
dias = [dia for dia in ordem_dias if dia in contagem_por_dia]
contagens = [contagem_por_dia[dia] for dia in dias]

usuarios_unicos = len(usuarios)
cidades_diferentes = len(cidades)

# Exporta também agrupamento por número para uso na rota /historico
conversas_por_numero = dict(conversas_por_numero)