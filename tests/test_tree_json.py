import json
import matplotlib.pyplot as plt
import networkx as nx

# Charger la structure JSON à partir du fichier
with open('./output/f161_1_projected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def json_to_networkx(data, parent=None):
    G = nx.DiGraph()

    def add_edges(data, parent=None):
        if isinstance(data, dict):
            for key, value in data.items():
                node_label = f"{parent}.{key}" if parent else key
                G.add_node(node_label)
                if parent:
                    G.add_edge(parent, node_label)
                add_edges(value, node_label)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                node_label = f"{parent}[{index}]"
                G.add_node(node_label)
                if parent:
                    G.add_edge(parent, node_label)
                add_edges(item, node_label)

    add_edges(data)
    return G

G = json_to_networkx(data)
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=1.5, iterations=50)  # Ajustez k et iterations pour une meilleure disposition
nx.draw(G, pos, with_labels=True, arrows=True, node_size=3000, node_color="skyblue", font_size=8, font_weight="bold")
plt.title("Représentation de la structure JSON")
plt.show()
