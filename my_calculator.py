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

def factorielle(n):
    """Calcule la factorielle de n"""
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    
    resultat = 1
    for i in range(2, int(n) + 1):
        resultat *= i
    return resultat

def degres_vers_radians(degres):
    """Convertit des degrés en radians"""
    PI = 3.14159265358979323846
    return degres * PI / 180

def radians_vers_degres(radians):
    """Convertit des radians en degrés"""
    PI = 3.14159265358979323846
    return radians * 180 / PI

def sinus(x, en_degres=False):
    """Calcule le sinus de x (utilise série de Taylor)"""
    if en_degres:
        x = degres_vers_radians(x)
    
    # Normaliser x dans [-2π, 2π]
    PI = 3.14159265358979323846
    deux_pi = 2 * PI
    while x > PI:
        x -= deux_pi
    while x < -PI:
        x += deux_pi
    
    # Série de Taylor: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
    terme = x
    somme = terme
    
    for n in range(1, 20):  # 20 termes pour la précision
        terme *= -x * x / ((2 * n) * (2 * n + 1))
        somme += terme
    
    return somme

def cosinus(x, en_degres=False):
    """Calcule le cosinus de x (utilise série de Taylor)"""
    if en_degres:
        x = degres_vers_radians(x)
    
    # Normaliser x dans [-2π, 2π]
    PI = 3.14159265358979323846
    deux_pi = 2 * PI
    while x > PI:
        x -= deux_pi
    while x < -PI:
        x += deux_pi
    
    # Série de Taylor: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
    terme = 1
    somme = terme
    
    for n in range(1, 20):  # 20 termes pour la précision
        terme *= -x * x / ((2 * n - 1) * (2 * n))
        somme += terme
    
    return somme

def tangente(x, en_degres=False):
    """Calcule la tangente de x"""
    cos_x = cosinus(x, en_degres)
    if abs(cos_x) < 0.0000001:  # Proche de zéro
        return None  # Tangente indéfinie
    return sinus(x, en_degres) / cos_x

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

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("CALCULATRICE SCIENTIFIQUE PYTHON")
    print("="*50)
    print("1. Calcul basique (+, -, *, /, **)")
    print("2. Trigonométrie (sin, cos, tan)")
    print("3. Factorielle")
    print("4. Voir l'historique")
    print("5. Effacer l'historique")
    print("6. Quitter")
    print("="*50)

def menu_trigonometrie(historique):
    """Menu pour les fonctions trigonométriques"""
    print("\n--- TRIGONOMÉTRIE ---")
    print("1. Sinus")
    print("2. Cosinus")
    print("3. Tangente")
    print("4. Retour")
    
    choix = input("Votre choix : ")
    
    if choix in ['1', '2', '3']:
        angle = demander_nombre("Entrez l'angle : ")
        unite = input("En degrés (d) ou radians (r) ? : ").lower()
        en_degres = (unite == 'd')
        
        if choix == '1':
            resultat = sinus(angle, en_degres)
            operation = f"sin({angle}{'°' if en_degres else ' rad'}) = {resultat}"
        elif choix == '2':
            resultat = cosinus(angle, en_degres)
            operation = f"cos({angle}{'°' if en_degres else ' rad'}) = {resultat}"
        else:
            resultat = tangente(angle, en_degres)
            if resultat is None:
                print("\nErreur : Tangente indéfinie pour cet angle !")
                return
            operation = f"tan({angle}{'°' if en_degres else ' rad'}) = {resultat}"
        
        print(f"\nRésultat : {operation}")
        historique.append(operation)

def main():
    """Fonction principale du programme"""
    historique = []
    
    print("Bienvenue dans la Calculatrice Scientifique Python !")
    print("Tous les calculs sont effectués sans librairie mathématique.")
    
    while True:
        afficher_menu()
        choix = input("Votre choix : ")
        
        if choix == '1':
            # Calcul basique
            print("\nOpérations disponibles : +, -, *, /, ** (puissance)")
            
            nombre1 = demander_nombre("Entrez le premier nombre : ")
            operateur = input("Entrez l'opérateur : ")
            nombre2 = demander_nombre("Entrez le deuxième nombre : ")
            
            # Normaliser l'opérateur avant de calculer
            operateur_original = operateur
            if operateur == 'x':
                operateur = '*'
            elif operateur == '÷':
                operateur = '/'
            elif operateur == '^':
                operateur = '**'
            
            resultat = calculer(nombre1, nombre2, operateur)
            
            if resultat is None:
                if operateur not in ['+', '-', '*', '/', '**']:
                    print(f"\nErreur : Opérateur '{operateur_original}' non reconnu !")
                else:
                    print("\nErreur : Division par zéro impossible !")
            else:
                operation = f"{nombre1} {operateur} {nombre2} = {resultat}"
                print(f"\nRésultat : {operation}")
                historique.append(operation)
        
        elif choix == '2':
            # Trigonométrie
            menu_trigonometrie(historique)
        
        elif choix == '3':
            # Factorielle
            nombre = demander_nombre("Entrez un nombre entier positif : ")
            resultat = factorielle(nombre)
            
            if resultat is None:
                print("\nErreur : La factorielle n'existe pas pour les nombres négatifs !")
            else:
                operation = f"{int(nombre)}! = {resultat}"
                print(f"\nRésultat : {operation}")
                historique.append(operation)
        
        elif choix == '4':
            # Afficher l'historique
            afficher_historique(historique)
        
        elif choix == '5':
            # Effacer l'historique
            if len(historique) > 0:
                confirmation = input("\nÊtes-vous sûr de vouloir effacer l'historique ? (o/n) : ")
                if confirmation.lower() == 'o' or confirmation.lower() == 'oui':
                    historique.clear()
                    print("L'historique a été effacé avec succès.")
                else:
                    print("Opération annulée.")
            else:
                print("\nL'historique est déjà vide.")
        
        elif choix == '6':
            # Quitter
            print("\nMerci d'avoir utilisé la Calculatrice Scientifique Python !")
            print("À bientôt !")
            break
        
        else:
            print("\nErreur : Choix invalide. Veuillez choisir entre 1 et 6.")

# Lancement du programme
if __name__ == "__main__":
    main()