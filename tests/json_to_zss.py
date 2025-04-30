import json
from zss import distance, Node
from nltk.metrics import edit_distance

# Fonction pour convertir une structure JSON en arbre zss.Node
def json_to_zss_node(data, label=None):
    if label is None:
        label = "root"
    node = Node(label)

    if isinstance(data, dict):
        for key, value in data.items():
            child_node = json_to_zss_node(value, key)
            node.addkid(child_node)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            child_node = json_to_zss_node(item, str(index))
            node.addkid(child_node)
    return node

# Fonction de coût de mise à jour personnalisée
def update_cost(node1, node2):
    return edit_distance(node1.label, node2.label)

# Fonction de coût d'insertion et de suppression personnalisée
def insert_and_remove_cost(node):
    return len(node.label)

# Charger les fichiers JSON
with open('../output/f161_1_projected.json', 'r', encoding='utf-8') as file1:
    data1 = json.load(file1)

with open('../output/test_bruit.json', 'r', encoding='utf-8') as file2:
    data2 = json.load(file2)

# Convertir les structures JSON en arbres zss.Node
tree1 = json_to_zss_node(data1)
tree2 = json_to_zss_node(data2)

# Calculer la distance entre les deux arbres avec des coûts personnalisés
distance_value = distance(
    tree1,
    tree2,
    get_children=Node.get_children,
    insert_cost=insert_and_remove_cost,
    remove_cost=insert_and_remove_cost,
    update_cost=update_cost,
    return_operations=False
)

print(f"Distance entre les deux arbres : {distance_value}")
