import random
import string

# Fonction pour générer un mot aléatoire
def generate_random_word():
    # Détermine la longueur aléatoire du mot entre 1 et 20 caractères
    length = random.randint(0, 20)
    
    # Génère un mot aléatoire de la longueur déterminée
    letters = string.ascii_letters
    random_word = ''.join(random.choice(letters) for _ in range(length))
    
    return random_word

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

# Initialisation du compteur
verified_count = 0
violated_count = 0

# Exécuter le test dix-mille fois
for _ in range(10000):
    # Trois chaînes au choix
    A = generate_random_word()
    B = generate_random_word()
    C = generate_random_word()

    # print(A, B, C)

    # Calcul des distances de Levenshtein
    d_AB = levenshtein_distance(A, B)
    d_BC = levenshtein_distance(B, C)
    d_AC = levenshtein_distance(A, C)

    # Vérification de l'inégalité triangulaire
    if d_AC <= d_AB + d_BC:
        verified_count += 1
    else:
        violated_count += 1

print(verified_count, violated_count)