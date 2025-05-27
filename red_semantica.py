from SPARQLWrapper import SPARQLWrapper, JSON
import networkx as nx
import matplotlib.pyplot as plt

# Esto crea el grafo dirigido
G = nx.DiGraph()

# ------------------------
# 1. Información del ejercicio
# ------------------------
triples = [
    ("Persona", "tiene", "Brazo"),
    ("Persona", "tiene", "Pierna"),
    ("Persona", "puede_ser", "Hombre"),
    ("Persona", "puede_ser", "Mujer"),
    ("Jugador_Baloncesto", "es_un", "Hombre"),
    ("Michael_Jordan", "es_un", "Jugador_Baloncesto"),
    ("Michael_Jordan", "juega_de", "Escolta"),
    ("Shaquille_ONeil", "es_un", "Jugador_Baloncesto"),
    ("Shaquille_ONeil", "juega_de", "Pivot"),
    ("Escolta", "media_puntos", "20"),
    ("Michael_Jordan", "media_puntos", "20"),
    ("Pivot", "media_puntos", "20"),
    ("Jugador_Baloncesto", "peso", "120_kilos"),
    ("Michael_Jordan", "pertenece_a", "Bulls"),
    ("Shaquille_ONeil", "pertenece_a", "Lakers"),
]

# Esto agrega los nodos y relaciones al grafo
for sujeto, predicado, objeto in triples:
    G.add_node(sujeto)
    G.add_node(objeto)
    G.add_edge(sujeto, objeto, label=predicado)

# ------------------------
# 2. Consulta a Wikidata
# ------------------------

# Aqui consulta: equipos en los que jugó Michael Jordan (Q41421)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

query = """
SELECT ?teamLabel WHERE {
  wd:Q41421 wdt:P54 ?team.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""
sparql.setQuery(query)
results = sparql.query().convert()

# Esto agrega los equipos reales al grafo
for result in results["results"]["bindings"]:
    equipo = result["teamLabel"]["value"]
    G.add_node(equipo)
    G.add_edge("Michael_Jordan", equipo, label="jugó_en (Wikidata)")

# ------------------------
# 3. Dibuja el grafo
# ------------------------
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(16, 12))

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Red Semántica con datos de Wikidata", fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.show()
