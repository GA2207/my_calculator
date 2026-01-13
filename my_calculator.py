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

# Math Calcul
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
    # Test avec entrée utilisateur
    print("Test de la calculatrice basique")
    nombre1 = demander_nombre("Premier nombre : ")
    operateur = input("Opérateur (+, -, *, /, **) : ")
    nombre2 = demander_nombre("Deuxième nombre : ")
    
    resultat = calculer(nombre1, nombre2, operateur)
    if resultat is not None:
        print(f"Résultat : {nombre1} {operateur} {nombre2} = {resultat}")
    else:
        print("Erreur dans le calcul")
    # Tests basiques
    print("Test addition:", additionner(5, 3))
    print("Test soustraction:", soustraire(10, 4))
    print("Test multiplication:", multiplier(6, 7))
    print("Test division:", diviser(20, 4))
    print("Test puissance:", puissance(2, 3))
