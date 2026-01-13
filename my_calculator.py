# 1) Erreur personnalisée
class CalcError(Exception):
    pass


# 2) Lire un nombre
def ask_number(message):
    while True:
        s = input(message).strip()
        s = s.replace(",", ".")

        if s == "":
            print("Erreur : vous devez entrer un nombre.")
            continue

        try:
            return float(s)
        except:
            print("Erreur : entrée invalide (ex: 12, 12.5, -3)")


# 3) Choisir une opération
def ask_operation():
    while True:
        print("\nOpérations disponibles :")
        print(" +  Addition")
        print(" -  Soustraction")
        print(" *  Multiplication")
        print(" /  Division")
        print(" %  Modulo")
        print(" ** Puissance (exposant entier)")

        op = input("Choisissez une opération : ").strip()

        if op in ["+", "-", "*", "/", "%", "**"]:
            return op

        print("Erreur : opération invalide.")


# 4) Calcul
def compute(a, b, op):
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

    if op == "%":
        if b == 0:
            raise CalcError("Modulo par zéro interdit.")
        return a % b

    if op == "**":
        # exposant entier uniquement
        if b != int(b):
            raise CalcError("La puissance doit être un entier.")
        if abs(b) > 1000:
            raise CalcError("Puissance trop grande.")
        return a ** int(b)

    raise CalcError("Opération inconnue.")


# 5) Affichage propre
def pretty_number(x):
    if x == int(x):
        return str(int(x))

    s = str(x)
    if "." in s:
        while s.endswith("0"):
            s = s[:-1]
        if s.endswith("."):
            s = s[:-1]
    return s


# 6) Menu
def show_menu():
    print("\n===== MENU =====")
    print("1) Faire un calcul")
    print("2) Voir l'historique")
    print("3) Effacer l'historique")
    print("4) Quitter")


def ask_choice():
    while True:
        c = input("Votre choix (1-4) : ").strip()
        if c in ["1", "2", "3", "4"]:
            return c
        print("Erreur : choisissez entre 1 et 4.")


# 7) Programme principal
def main():
    history = []

    print("=== Calculatrice MENU (sans import) ===")

    while True:
        show_menu()
        choice = ask_choice()

        # ---- calcul ----
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
                print("Erreur :", e)

        # ---- historique ----
        elif choice == "2":
            if len(history) == 0:
                print("Historique vide.")
            else:
                print("\n--- Historique ---")
                for i in range(len(history)):
                    print(str(i + 1) + ") " + history[i])

        # ---- effacer historique ----
        elif choice == "3":
            history = []
            print("Historique effacé.")

        # ---- quitter ----
        elif choice == "4":
            print("Au revoir.")
            break


if __name__ == "__main__":
    main()
