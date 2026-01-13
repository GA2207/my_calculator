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

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("CALCULATRICE PYTHON")
    print("="*50)
    print("1. Effectuer un calcul")
    print("2. Voir l'historique")
    print("3. Effacer l'historique")
    print("4. Quitter")
    print("="*50)

def main():
    """Fonction principale du programme"""
    historique = []
    
    print("Bienvenue dans la Calculatrice Python !")
    print("Vous pouvez effectuer des calculs simples.")
    
    while True:
        afficher_menu()
        choix = input("Votre choix : ")
        
        if choix == '1':
            # Effectuer un calcul
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
                # Affichage du résultat
                operation = f"{nombre1} {operateur} {nombre2} = {resultat}"
                print(f"\nRésultat : {operation}")
                historique.append(operation)
        
        elif choix == '2':
            # Afficher l'historique
            afficher_historique(historique)
        
        elif choix == '3':
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
        
        elif choix == '4':
            # Quitter
            print("\nMerci d'avoir utilisé la Calculatrice Python !")
            print("À bientôt !")
            break
        
        else:
            print("\nErreur : Choix invalide. Veuillez choisir entre 1 et 4.")

# Lancement du programme
if __name__ == "__main__":
    main()