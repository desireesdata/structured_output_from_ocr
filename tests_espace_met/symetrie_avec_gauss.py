import numpy as np
from scipy.ndimage import gaussian_filter

def filtrage_adaptatif(D, sigma=1.0, seuil=-0.1):
    """
    Applique un filtrage local adaptatif sur la matrice de distance D
    en utilisant une convolution gaussienne.
    """
    # Moyenne locale des distances
    D_smooth = gaussian_filter(D, sigma=sigma)

    # Contraste local
    E = D - D_smooth

    # Seuil : ne garder que les minima locaux suffisamment marqués
    mask = E < seuil

    return mask, E

# Exemple : matrice D simulée
np.random.seed(0)
D = np.random.rand(10, 12)  # matrice distance aléatoire bruitée
D[3, 5] = 0.01  # vrai minimum pour test
D[6, 9] = 0.02

mask, E = filtrage_adaptatif(D, sigma=1.0, seuil=-0.05)

# Affichage des appariements conservés
appariements = np.argwhere(mask)
print("Appariements fiables (indices i, j):", appariements)
