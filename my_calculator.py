# 1) Erreur personnalisée
class CalcError(Exception):
    pass


# 2) Lire un nombre (entier ou décimal)
def ask_number(message):
    """
    Demande un nombre à l'utilisateur.
    Répète tant que l'entrée n'est pas un nombre.
    """
    while True:
        s = input(message).strip()

        # Remplacer une virgule par un point (pratique en France)
        s = s.replace(",", ".")

        if s == "":
            print("Erreur : vous devez entrer un nombre.")
            continue

        # conversion en float (sans import)
        try:
            return float(s)
        except:
            print("Erreur : entrée invalide. Exemple : 12  ou  12.5  ou  -3.2")


# 3) Choisir une opération
def ask_operation():
    """
    Demande une opération parmi + - * /
    """
    while True:
        op = input("Choisissez une opération (+, -, *, /) : ").strip()
        if op in ["+", "-", "*", "/"]:
            return op
        print("Erreur : opération invalide. Choisissez uniquement +, -, * ou /.")


# 4) Calculer le résultat
def compute(a, b, op):
    """
    Effectue le calcul a (op) b avec gestion des erreurs.
    """
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise CalcError("Division par zéro interdite.")
        return a / b

    # Normalement on ne passe jamais ici car ask_operation filtre déjà
    raise CalcError("Opération inconnue.")


# 5) Affichage "propre" d'un float
def pretty_number(x):
    # Si x est un entier (ex: 5.0), afficher 5
    if x == int(x):
        return str(int(x))

    # Sinon on affiche en supprimant les zéros inutiles
    s = str(x)
    if "." in s:
        while s.endswith("0"):
            s = s[:-1]
        if s.endswith("."):
            s = s[:-1]
    return s


# 6) Afficher le menu
def show_menu():
    print("\n===== MENU =====")
    print("1) Faire un calcul")
    print("2) Voir l'historique")
    print("3) Effacer l'historique")
    print("4) Quitter")


def ask_choice():
    """
    Demande un choix 1-4.
    """
    while True:
        choice = input("Votre choix (1-4) : ").strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("Erreur : choisissez un chiffre entre 1 et 4.")


# 7) Programme principal
def main():
    history = []  # liste de chaînes, ex: "2 + 3 = 5"

    print("=== Calculatrice MENU (sans import) ===")

    while True:
        show_menu()
        choice = ask_choice()

        # 1) calcul
        if choice == "1":
            a = ask_number("Entrez le premier nombre : ")
            b = ask_number("Entrez le deuxième nombre : ")
            op = ask_operation()

            try:
                result = compute(a, b, op)
                line = (
                    pretty_number(a)
                    + " " + op + " "
                    + pretty_number(b)
                    + " = "
                    + pretty_number(result)
                )

                print("Résultat :", pretty_number(result))
                history.append(line)

            except CalcError as e:
                print("Erreur :", str(e))

        # 2) historique
        elif choice == "2":
            if len(history) == 0:
                print("Historique vide.")
            else:
                print("\n--- Historique ---")
                for i in range(len(history)):
                    print(str(i + 1) + ") " + history[i])

        # 3) effacer historique
        elif choice == "3":
            history = []
            print("Historique effacé.")

        # 4) quitter
        elif choice == "4":
            print("Au revoir.")
            break


if __name__ == "__main__":
    main()
