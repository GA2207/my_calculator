# Calculatrice Python - Version Console
# Projet développé sans module Math ni eval()

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

if __name__ == "__main__":
    # Tests basiques
    print("Test addition:", additionner(5, 3))
    print("Test soustraction:", soustraire(10, 4))
    print("Test multiplication:", multiplier(6, 7))
    print("Test division:", diviser(20, 4))
    print("Test puissance:", puissance(2, 3))