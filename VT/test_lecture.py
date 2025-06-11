import numpy as np
import plotly.graph_objects as go

# Charger la matrice depuis le fichier .npy
file_path = 'A_1_OCR_corrige.npy'  # Remplacez par le chemin de votre fichier
matrix = np.load(file_path)

# Créer une visualisation de la matrice avec Plotly
fig = go.Figure(data=go.Heatmap(
    z=matrix,
    colorscale='Viridis',  # Vous pouvez changer la palette de couleurs
))

# Mettre à jour la mise en page pour une meilleure visualisation
fig.update_layout(
    title='Visualisation de la Matrice',
    xaxis_title='Colonnes',
    yaxis_title='Lignes',
)

# Afficher la figure
fig.show()
