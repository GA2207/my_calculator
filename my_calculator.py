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


# 3) Choisir une opération (AJOUT des opérations mathématiques)
def ask_operation():
    while True:
        print("\nOpérations disponibles :")
        print(" +   Addition")
        print(" -   Soustraction")
        print(" *   Multiplication")
        print(" /   Division")
        print(" %   Modulo")
        print(" **  Puissance (exposant entier)")
        # --- AJOUTS ---
        print(" //  Division entière")
        print(" √   Racine carrée (utilise seulement le 1er nombre)")
        print(" !   Factorielle (utilise seulement le 1er nombre)")
        print(" abs Valeur absolue (utilise seulement le 1er nombre)")
        print(" neg Opposé (utilise seulement le 1er nombre)")
        print(" inv Inverse 1/a (utilise seulement le 1er nombre)")
        print(" min Minimum (a, b)")
        print(" max Maximum (a, b)")
        print(" avg Moyenne (a, b)")
        print(" round Arrondi (a, b = nb de décimales entier)")
        print(" floor Arrondi inférieur (utilise seulement le 1er nombre)")
        print(" ceil Arrondi supérieur (utilise seulement le 1er nombre)")

        op = input("Choisissez une opération : ").strip()

        if op in [
            "+", "-", "*", "/", "%", "**",
            "//", "√", "!", "abs", "neg", "inv",
            "min", "max", "avg", "round", "floor", "ceil"
        ]:
            return op

        print("Erreur : opération invalide.")


# --- AJOUT : fonctions mathématiques internes (sans import) ---
def _is_integer(x):
    return x == int(x)

def _factorial(n):
    if n < 0:
        raise CalcError("Factorielle impossible pour n < 0.")
    if n > 2000:
        raise CalcError("Factorielle trop grande.")
    r = 1
    i = 2
    while i <= n:
        r *= i
        i += 1
    return r

def _sqrt(x):
    if x < 0:
        raise CalcError("Racine carrée d’un nombre négatif interdite.")
    if x == 0:
        return 0.0
    g = x if x >= 1 else 1.0
    i = 0
    while i < 50:
        g = (g + x / g) / 2.0
        i += 1
    return g

def _floor(x):
    i = int(x)  # tronque vers 0
    return i if x >= 0 or x == i else i - 1

def _ceil(x):
    i = int(x)  # tronque vers 0
    return i if x <= 0 or x == i else i + 1


# 4) Calcul (AJOUT des opérations mathématiques)
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

    # --- AJOUTS ---
    if op == "//":
        if b == 0:
            raise CalcError("Division entière par zéro.")
        return _floor(a / b)

    if op == "√":
        return _sqrt(a)

    if op == "!":
        if not _is_integer(a):
            raise CalcError("Factorielle : entier requis.")
        return _factorial(int(a))

    if op == "abs":
        return a if a >= 0 else -a

    if op == "neg":
        return -a

    if op == "inv":
        if a == 0:
            raise CalcError("Inverse de zéro interdit.")
        return 1 / a

    if op == "min":
        return a if a <= b else b

    if op == "max":
        return a if a >= b else b

    if op == "avg":
        return (a + b) / 2

    if op == "round":
        if not _is_integer(b):
            raise CalcError("Arrondi : décimales entières.")
        n = int(b)
        if abs(n) > 12:
            raise CalcError("Arrondi : trop de décimales (max 12).")

        p = 10 ** abs(n)

        if n >= 0:
            x = a * p
            if x >= 0:
                x = int(x + 0.5)
            else:
                x = int(x - 0.5)
            return x / p
        else:
            x = a / p
            if x >= 0:
                x = int(x + 0.5)
            else:
                x = int(x - 0.5)
            return x * p

    if op == "floor":
        return _floor(a)

    if op == "ceil":
        return _ceil(a)

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

                # affichage ligne historique
                unary_ops = ["√", "!", "abs", "neg", "inv", "floor", "ceil"]
                if op in unary_ops:
                    line = op + "(" + pretty_number(a) + ") = " + pretty_number(result)
                elif op == "round":
                    line = "round(" + pretty_number(a) + ", " + pretty_number(b) + ") = " + pretty_number(result)
                else:
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
