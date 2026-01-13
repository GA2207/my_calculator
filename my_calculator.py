# Calculatrice Python - Version Console
# Projet développé sans module Math ni eval()

def demander_nombre(message):
    """Demande un nombre à l'utilisateur et gère les erreurs"""
    while True:
        try:
            entree = input(message)
            if '.' in entree or ',' in entree:
                entree = entree.replace(',', '.')
                return float(entree)
            else:
                return int(entree)
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide !")

def additionner(a, b):
    """Additionne deux nombres"""
    return a + b

def soustraire(a, b):
    """Soustrait deux nombres"""
    return a - b

def multiplier(a, b):
    """Multiplie deux nombres"""
    return a * b

def diviser(a, b):
    """Divise deux nombres avec gestion de la division par zéro"""
    if b == 0:
        return None
    return a / b

def puissance(a, b):
    """Calcule a à la puissance b"""
    resultat = 1
    exposant = int(b) if b >= 0 else int(-b)
    
    for _ in range(exposant):
        resultat *= a
    
    if b < 0:
        return 1 / resultat
    return resultat

def afficher_historique(historique):
    """Affiche l'historique des calculs"""
    if len(historique) == 0:
        print("\nAucun calcul dans l'historique.")
    else:
        print("\n" + "="*50)
        print("HISTORIQUE DES CALCULS")
        print("="*50)
        for i, operation in enumerate(historique, 1):
            print(f"{i}. {operation}")
        print("="*50)

def calculer(nombre1, nombre2, operateur):
    """Effectue le calcul selon l'opérateur choisi"""
    if operateur == '+':
        return additionner(nombre1, nombre2)
    elif operateur == '-':
        return soustraire(nombre1, nombre2)
    elif operateur == '*' or operateur == 'x':
        return multiplier(nombre1, nombre2)
    elif operateur == '/' or operateur == '÷':
        return diviser(nombre1, nombre2)
    elif operateur == '**' or operateur == '^':
        return puissance(nombre1, nombre2)
    else:
        return None

if __name__ == "__main__":
    # Test de l'historique
    historique = []
    
    # Simulation de quelques calculs
    historique.append("5 + 3 = 8")
    historique.append("10 - 4 = 6")
    historique.append("6 * 7 = 42")
    
    afficher_historique(historique)
    
    # Test d'effacement
    historique.clear()
    print("\nAprès effacement :")
    afficher_historique(historique)