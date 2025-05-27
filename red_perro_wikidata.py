import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Añade los nodos y relaciones (red semántica del perro)
G.add_edge("Perro", "Mamífero", label="es un")
G.add_edge("Perro", "Cola", label="tiene parte")
G.add_edge("Mamífero", "Animal", label="subclase de")
G.add_edge("Animal", "Canis lupus familiaris", label="ejemplo de")
G.add_edge("Canis lupus familiaris", "Doméstico", label="habita en")
G.add_edge("Doméstico", "Humano", label="relacionado con")

# Dibujar
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 7))

nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Red Semántica: Perro (Wikidata-style)", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
