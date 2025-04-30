import matplotlib.pyplot as plt
import networkx as nx
from zss import simple_distance, Node

# Illustration graphes simples pour distances TED 
# Définir les arbres A et B
A = (
    Node("f")
    .addkid(Node("a")
        .addkid(Node("h"))
        .addkid(Node("c")
            .addkid(Node("l"))))
    .addkid(Node("e"))
)

B = (
    Node("f")
    .addkid(Node("a")
        .addkid(Node("d"))
        .addkid(Node("c")
            .addkid(Node("b"))))
    .addkid(Node("e"))
)

# Calculer et afficher la distance entre les arbres
distance = simple_distance(A, B)
print(f"Distance entre les arbres A et B : {distance}")

# VISUALISATION
def zss_to_networkx(node):
    G = nx.DiGraph()

    def add_edges(node):
        for kid in node.children:
            G.add_edge(node.label, kid.label)
            add_edges(kid)

    add_edges(node)
    return G

# Convertir les arbres A et B en graphes networkx
G_A = zss_to_networkx(A)
G_B = zss_to_networkx(B)

# Dessiner les graphes
plt.figure(figsize=(12, 6))

# Dessiner l'arbre A
plt.subplot(1, 2, 1)
pos = nx.spring_layout(G_A)
nx.draw(G_A, pos, with_labels=True, arrows=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Arbre A")

# Dessiner l'arbre B
plt.subplot(1, 2, 2)
pos = nx.spring_layout(G_B)
nx.draw(G_B, pos, with_labels=True, arrows=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Arbre B")

plt.show()

