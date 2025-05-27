from SPARQLWrapper import SPARQLWrapper, JSON
import networkx as nx
import matplotlib.pyplot as plt

# Conexión con Wikidata
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
query = """
SELECT ?item ?itemLabel ?prop ?propLabel WHERE {
  wd:Q144 ?p ?item.  # Q144 = Perro
  ?prop wikibase:directClaim ?p.
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "es".
    ?item rdfs:label ?itemLabel.
    ?prop rdfs:label ?propLabel.
  }
}
"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Crea el grafo
G = nx.DiGraph()
G.add_node("Perro", label="Perro")

for result in results["results"]["bindings"]:
    item_label = result["itemLabel"]["value"]
    prop_label = result["propLabel"]["value"]
    G.add_node(item_label, label=item_label)
    G.add_edge("Perro", item_label, label=prop_label)

# Dibuja el grafo
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(14, 10))

nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=9)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Red Semántica del Perro desde Wikidata", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
