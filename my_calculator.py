import matplotlib.pyplot as plt

def demander_nombre(message):
    while True:
        try:
            entree = input(message)
            if '.' in entree or ',' in entree:
                entree = entree.replace(',', '.')
                return float(entree)
            else:
                return int(entree)
        except ValueError:
            print("Erreur : entre un nombre valide stp !")

# Opérations basiques
def additionner(a, b):
    return a + b

def soustraire(a, b):
    return a - b

def multiplier(a, b):
    return a * b

def diviser(a, b):
    if b == 0:
        return None
    return a / b

def puissance(a, b):
    # Gère les puissances positives et négatives
    if b == 0:
        return 1

    resultat = 1
    exposant = abs(int(b))

    for _ in range(exposant):
        resultat *= a

    if b < 0:
        return 1 / resultat
    return resultat

def modulo(a, b):
    if b == 0:
        return None
    quotient = int(a / b)
    reste = a - (quotient * b)
    return reste

def factorielle(n):
    # Classique factorielle
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1

    resultat = 1
    for i in range(2, int(n) + 1):
        resultat *= i
    return resultat

def racine_carree(n, precision=0.000001):
    # Méthode de Newton pour la racine carrée
    # x_nouveau = (x + n/x) / 2
    if n < 0:
        return None
    if n == 0:
        return 0

    x = n
    while True:
        racine = (x + n / x) / 2
        if abs(racine - x) < precision:
            return racine
        x = racine

def racine_n(nombre, n, precision=0.000001):
    # Racine n-ième avec Newton aussi
    if n == 0:
        return None
    if nombre < 0 and n % 2 == 0:
        return None

    if nombre == 0:
        return 0

    negatif = False
    if nombre < 0:
        negatif = True
        nombre = -nombre

    x = nombre
    for _ in range(100):
        x_nouveau = ((n - 1) * x + nombre / puissance(x, n - 1)) / n
        if abs(x_nouveau - x) < precision:
            return -x_nouveau if negatif else x_nouveau
        x = x_nouveau

    return -x if negatif else x

def valeur_absolue(n):
    if n < 0:
        return -n
    return n

def logarithme_naturel(x, precision=0.000001):
    # ln par série de Taylor - j'ai galéré sur celui-là
    if x <= 0:
        return None

    # Pour x proche de 1, formule : ln(x) = 2 * [(x-1)/(x+1) + 1/3*((x-1)/(x+1))^3 + ...]
    if 0.5 < x < 2:
        y = (x - 1) / (x + 1)
        y_carre = y * y
        resultat = 0
        terme = y

        for n in range(1, 100, 2):
            resultat += terme / n
            terme *= y_carre
            if abs(terme / n) < precision:
                break

        return 2 * resultat

    elif x >= 2:
        # Réduction en divisant par e
        compteur = 0
        E = 2.718281828459045
        while x > 2:
            x /= E
            compteur += 1
        return compteur + logarithme_naturel(x, precision)

    else:
        # Pour x < 0.5 : ln(x) = -ln(1/x)
        return -logarithme_naturel(1 / x, precision)

def logarithme_base(x, base):
    # log_base(x) = ln(x) / ln(base)
    if x <= 0 or base <= 0 or base == 1:
        return None

    ln_x = logarithme_naturel(x)
    ln_base = logarithme_naturel(base)

    if ln_x is None or ln_base is None:
        return None

    return ln_x / ln_base

def exponentielle(x, precision=0.000001):
    # e^x avec série de Taylor : e^x = 1 + x + x²/2! + x³/3! + ...
    resultat = 1
    terme = 1

    for n in range(1, 100):
        terme *= x / n
        resultat += terme
        if abs(terme) < precision:
            break

    return resultat

# Conversions angles
def degres_vers_radians(degres):
    PI = 3.14159265358979323846
    return degres * PI / 180

def radians_vers_degres(radians):
    PI = 3.14159265358979323846
    return radians * 180 / PI

def sinus(x, en_degres=False):
    # sin avec série de Taylor
    if en_degres:
        x = degres_vers_radians(x)

    # Normaliser dans [-2π, 2π]
    PI = 3.14159265358979323846
    deux_pi = 2 * PI
    while x > PI:
        x -= deux_pi
    while x < -PI:
        x += deux_pi

    # sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
    terme = x
    somme = terme

    for n in range(1, 20):
        terme *= -x * x / ((2 * n) * (2 * n + 1))
        somme += terme

    return somme

def cosinus(x, en_degres=False):
    # cos avec série de Taylor
    if en_degres:
        x = degres_vers_radians(x)

    PI = 3.14159265358979323846
    deux_pi = 2 * PI
    while x > PI:
        x -= deux_pi
    while x < -PI:
        x += deux_pi

    # cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
    terme = 1
    somme = terme

    for n in range(1, 20):
        terme *= -x * x / ((2 * n - 1) * (2 * n))
        somme += terme

    return somme

def tangente(x, en_degres=False):
    # tan = sin/cos
    cos_x = cosinus(x, en_degres)
    if abs(cos_x) < 0.0000001:
        return None
    return sinus(x, en_degres) / cos_x

def arcsinus(x, precision=0.000001):
    # arcsin par série de Taylor
    if x < -1 or x > 1:
        return None

    if x == 1:
        return 3.14159265358979323846 / 2
    if x == -1:
        return -3.14159265358979323846 / 2

    resultat = x
    terme = x
    x_carre = x * x

    for n in range(1, 50):
        terme *= x_carre * (2 * n - 1) * (2 * n - 1) / ((2 * n) * (2 * n + 1))
        resultat += terme
        if abs(terme) < precision:
            break

    return resultat

def arccosinus(x):
    # arccos(x) = π/2 - arcsin(x)
    arcsin_x = arcsinus(x)
    if arcsin_x is None:
        return None
    PI = 3.14159265358979323846
    return PI / 2 - arcsin_x

def arctangente(x, precision=0.000001):
    # arctan par série de Taylor
    if x > 1:
        PI = 3.14159265358979323846
        return PI / 2 - arctangente(1 / x, precision)
    if x < -1:
        PI = 3.14159265358979323846
        return -PI / 2 - arctangente(1 / x, precision)

    # arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    resultat = 0
    terme = x
    x_carre = x * x

    for n in range(50):
        resultat += terme / (2 * n + 1)
        terme *= -x_carre
        if abs(terme / (2 * n + 3)) < precision:
            break

    return resultat

# Stats
def moyenne(liste):
    if len(liste) == 0:
        return None

    somme = 0
    for nombre in liste:
        somme += nombre

    return somme / len(liste)

def mediane(liste):
    if len(liste) == 0:
        return None

    # Tri à bulles (j'ai pas trouvé plus simple)
    liste_triee = liste.copy()
    n = len(liste_triee)

    for i in range(n):
        for j in range(0, n - i - 1):
            if liste_triee[j] > liste_triee[j + 1]:
                liste_triee[j], liste_triee[j + 1] = liste_triee[j + 1], liste_triee[j]

    if n % 2 == 0:
        return (liste_triee[n // 2 - 1] + liste_triee[n // 2]) / 2
    else:
        return liste_triee[n // 2]

def ecart_type(liste):
    if len(liste) == 0:
        return None

    moy = moyenne(liste)
    somme_carres = 0

    for nombre in liste:
        difference = nombre - moy
        somme_carres += difference * difference

    variance = somme_carres / len(liste)
    return racine_carree(variance)

def minimum(liste):
    if len(liste) == 0:
        return None

    min_val = liste[0]
    for nombre in liste:
        if nombre < min_val:
            min_val = nombre

    return min_val

def maximum(liste):
    if len(liste) == 0:
        return None

    max_val = liste[0]
    for nombre in liste:
        if nombre > max_val:
            max_val = nombre

    return max_val

# Combinatoire
def combinaison(n, k):
    # C(n,k) = n! / (k! * (n-k)!)
    if k < 0 or k > n:
        return None

    if k == 0 or k == n:
        return 1

    # Optimisation : C(n,k) = C(n, n-k)
    if k > n - k:
        k = n - k

    resultat = 1
    for i in range(k):
        resultat *= (n - i)
        resultat /= (i + 1)

    return int(resultat)

def arrangement(n, k):
    # A(n,k) = n! / (n-k)!
    if k < 0 or k > n:
        return None

    resultat = 1
    for i in range(n, n - k, -1):
        resultat *= i

    return int(resultat)

def est_premier(n):
    # Test de primalité simple
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Vérif jusqu'à racine(n)
    i = 3
    racine = int(racine_carree(n)) + 1
    while i <= racine:
        if n % i == 0:
            return False
        i += 2

    return True

def decomposition_premiers(n):
    # Décompose en facteurs premiers
    if n < 2:
        return []

    facteurs = []
    diviseur = 2

    while diviseur * diviseur <= n:
        while n % diviseur == 0:
            facteurs.append(diviseur)
            n //= diviseur
        diviseur += 1

    if n > 1:
        facteurs.append(n)

    return facteurs

def pgcd(a, b):
    # Algorithme d'Euclide
    a, b = int(abs(a)), int(abs(b))

    while b != 0:
        a, b = b, a % b

    return a

def ppcm(a, b):
    # PPCM via PGCD
    if a == 0 or b == 0:
        return 0

    return abs(a * b) // pgcd(a, b)

def afficher_historique(historique):
    if len(historique) == 0:
        print("\nAucun calcul dans l'historique.")
    else:
        print("\n" + "="*60)
        print("HISTORIQUE DES CALCULS")
        print("="*60)
        for i, operation in enumerate(historique, 1):
            print(f"{i}. {operation}")
        print("="*60)

def calculer(nombre1, nombre2, operateur):
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
    elif operateur == '%':
        return modulo(nombre1, nombre2)
    else:
        return None

def calculer_point_graphique(expression, x_val):
    """Analyseur manuel pour le graphique qui appelle TES fonctions (sans eval)."""
    exp = expression.replace(" ", "").lower()
    exp = exp.replace("**", "^")
    exp = exp.replace("x", f"({x_val})")

    # CORRECTION MULTIPLICATION IMPLICITE
    exp = exp.replace(")(", ")*(")

    tmp = ""
    for i in range(len(exp)):
        c = exp[i]
        if i > 0:
            prev = exp[i - 1]
            if c == '(' and (prev.isdigit() or prev == ')'):
                tmp += '*'
        tmp += c
    exp = tmp

    def resoudre(s):
        if not s:
            return 0

        while '(' in s:
            debut = s.find('(')

            nom_func = ""
            for f in ['sinus', 'cosinus', 'tangente', 'racine_carree', 'exponentielle', 'valeur_absolue']:
                if s[:debut].endswith(f):
                    nom_func = f
                    break

            niveau, fin = 0, -1
            for i in range(debut, len(s)):
                if s[i] == '(':
                    niveau += 1
                elif s[i] == ')':
                    niveau -= 1
                if niveau == 0:
                    fin = i
                    break

            res_int = resoudre(s[debut + 1:fin])

            if nom_func:
                if nom_func == 'sinus':
                    val = sinus(res_int)
                elif nom_func == 'cosinus':
                    val = cosinus(res_int)
                elif nom_func == 'tangente':
                    val = tangente(res_int)
                    if val is None:
                        return 0
                elif nom_func == 'racine_carree':
                    val = racine_carree(res_int)
                    if val is None:
                        return 0
                elif nom_func == 'exponentielle':
                    val = exponentielle(res_int)
                elif nom_func == 'valeur_absolue':
                    val = valeur_absolue(res_int)
                else:
                    val = res_int

                s = s[:debut - len(nom_func)] + str(val) + s[fin + 1:]
            else:
                s = s[:debut] + str(res_int) + s[fin + 1:]

        for i in range(len(s) - 1, -1, -1):
            if s[i] == '+' and i > 0 and s[i - 1] not in '*/^+-':
                return resoudre(s[:i]) + resoudre(s[i + 1:])
            if s[i] == '-' and i > 0 and s[i - 1] not in '*/^+-':
                return resoudre(s[:i]) - resoudre(s[i + 1:])

        for i in range(len(s) - 1, -1, -1):
            if s[i] == '*':
                return resoudre(s[:i]) * resoudre(s[i + 1:])
            if s[i] == '/':
                d = resoudre(s[i + 1:])
                return resoudre(s[:i]) / d if d != 0 else 0

        if '^' in s:
            b, e = s.split('^', 1)
            return puissance(resoudre(b), resoudre(e))

        try:
            return float(s)
        except:
            return 0

    return resoudre(exp)


def menu_graphique_original(historique):
    print("\n" + "="*60)
    print("TRACEUR DE COURBE SCIENTIFIQUE")
    print("="*60)
    print("Exemple : sinus(x) * 2 + x^2")
    expression = input("f(x) = ").replace("**", "^")

    x_min = demander_nombre("Valeur X min : ")
    x_max = demander_nombre("Valeur X max : ")

    if x_max == x_min:
        print("\nErreur : X max doit être différent de X min.")
        return
    if x_max < x_min:
        x_min, x_max = x_max, x_min

    liste_x, liste_y = [], []
    curr_x = x_min
    pas = (x_max - x_min) / 250

    while curr_x <= x_max:
        try:
            y = calculer_point_graphique(expression, curr_x)
            liste_x.append(curr_x)
            liste_y.append(y)
        except:
            pass
        curr_x += pas

    plt.figure(figsize=(10, 6))
    plt.plot(liste_x, liste_y, label=f"f(x) = {expression}")
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f"Graphique de la fonction : {expression}")
    plt.legend()
    plt.show()

    historique.append(f"Graphique : {expression}")

def afficher_menu():
    print("\n" + "="*60)
    print("CALCULATRICE SCIENTIFIQUE")
    print("="*60)
    print("1.  Calcul basique (+, -, *, /, **, %)")
    print("2.  Puissances et racines")
    print("3.  Trigonométrie")
    print("4.  Trigonométrie inverse")
    print("5.  Logarithmes et exponentielle")
    print("6.  Factorielle et combinatoire")
    print("7.  Statistiques")
    print("8.  Nombres premiers et PGCD/PPCM")
    print("9.  Voir l'historique")
    print("10. Effacer l'historique")
    print("11. Quitter")
    print("12. Tracer une courbe f(x)")
    print("="*60)

def menu_puissances_racines(historique):
    print("\n--- PUISSANCES ET RACINES ---")
    print("1. Racine carrée")
    print("2. Racine n-ième")
    print("3. Valeur absolue")
    print("4. Retour")

    choix = input("Choix : ")

    if choix == '1':
        nombre = demander_nombre("Nombre : ")
        resultat = racine_carree(nombre)

        if resultat is None:
            print("\nErreur : racine carrée d'un nombre négatif impossible !")
        else:
            operation = f"√{nombre} = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '2':
        nombre = demander_nombre("Nombre : ")
        n = int(demander_nombre("Indice de la racine : "))
        resultat = racine_n(nombre, n)

        if resultat is None:
            print("\nErreur : calcul impossible !")
        else:
            operation = f"{n}√{nombre} = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '3':
        nombre = demander_nombre("Nombre : ")
        resultat = valeur_absolue(nombre)
        operation = f"|{nombre}| = {resultat}"
        print(f"\nRésultat : {operation}")
        historique.append(operation)

def menu_trigonometrie(historique):
    print("\n--- TRIGONOMÉTRIE ---")
    print("1. Sinus")
    print("2. Cosinus")
    print("3. Tangente")
    print("4. Retour")

    choix = input("Choix : ")

    if choix in ['1', '2', '3']:
        angle = demander_nombre("Angle : ")
        unite = input("Degrés (d) ou radians (r) ? : ").lower()
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
                print("\nErreur : tangente indéfinie pour cet angle !")
                return
            operation = f"tan({angle}{'°' if en_degres else ' rad'}) = {resultat}"

        print(f"\nRésultat : {operation}")
        historique.append(operation)

def menu_trigonometrie_inverse(historique):
    print("\n--- TRIGONOMÉTRIE INVERSE ---")
    print("1. Arcsinus (sin⁻¹)")
    print("2. Arccosinus (cos⁻¹)")
    print("3. Arctangente (tan⁻¹)")
    print("4. Retour")

    choix = input("Choix : ")

    if choix in ['1', '2', '3']:
        valeur = demander_nombre("Valeur : ")

        if choix == '1':
            resultat = arcsinus(valeur)
            if resultat is None:
                print("\nErreur : valeur doit être entre -1 et 1 !")
                return
            operation = f"arcsin({valeur}) = {resultat} rad = {radians_vers_degres(resultat)}°"
        elif choix == '2':
            resultat = arccosinus(valeur)
            if resultat is None:
                print("\nErreur : valeur doit être entre -1 et 1 !")
                return
            operation = f"arccos({valeur}) = {resultat} rad = {radians_vers_degres(resultat)}°"
        else:
            resultat = arctangente(valeur)
            operation = f"arctan({valeur}) = {resultat} rad = {radians_vers_degres(resultat)}°"

        print(f"\nRésultat : {operation}")
        historique.append(operation)

def menu_logarithmes(historique):
    print("\n--- LOGARITHMES ET EXPONENTIELLE ---")
    print("1. Logarithme naturel (ln)")
    print("2. Logarithme base 10 (log)")
    print("3. Logarithme base quelconque")
    print("4. Exponentielle (e^x)")
    print("5. Retour")

    choix = input("Choix : ")

    if choix == '1':
        x = demander_nombre("x : ")
        resultat = logarithme_naturel(x)

        if resultat is None:
            print("\nErreur : ln n'existe que pour x > 0 !")
        else:
            operation = f"ln({x}) = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '2':
        x = demander_nombre("x : ")
        resultat = logarithme_base(x, 10)

        if resultat is None:
            print("\nErreur : log n'existe que pour x > 0 !")
        else:
            operation = f"log₁₀({x}) = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '3':
        x = demander_nombre("x : ")
        base = demander_nombre("Base : ")
        resultat = logarithme_base(x, base)

        if resultat is None:
            print("\nErreur : valeurs invalides !")
        else:
            operation = f"log_{base}({x}) = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '4':
        x = demander_nombre("x : ")
        resultat = exponentielle(x)
        operation = f"e^{x} = {resultat}"
        print(f"\nRésultat : {operation}")
        historique.append(operation)

def menu_factorielle_combinatoire(historique):
    print("\n--- FACTORIELLE ET COMBINATOIRE ---")
    print("1. Factorielle (n!)")
    print("2. Combinaison C(n,k)")
    print("3. Arrangement A(n,k)")
    print("4. Retour")

    choix = input("Choix : ")

    if choix == '1':
        n = demander_nombre("n : ")
        resultat = factorielle(n)

        if resultat is None:
            print("\nErreur : factorielle impossible pour nombres négatifs !")
        else:
            operation = f"{int(n)}! = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '2':
        n = int(demander_nombre("n : "))
        k = int(demander_nombre("k : "))
        resultat = combinaison(n, k)

        if resultat is None:
            print("\nErreur : k doit être entre 0 et n !")
        else:
            operation = f"C({n},{k}) = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

    elif choix == '3':
        n = int(demander_nombre("n : "))
        k = int(demander_nombre("k : "))
        resultat = arrangement(n, k)

        if resultat is None:
            print("\nErreur : k doit être entre 0 et n !")
        else:
            operation = f"A({n},{k}) = {resultat}"
            print(f"\nRésultat : {operation}")
            historique.append(operation)

def menu_statistiques(historique):
    print("\n--- STATISTIQUES ---")
    print("Entre une série de nombres séparés par des espaces")

    entree = input("Nombres : ")
    try:
        liste = [float(x) for x in entree.split()]

        if len(liste) == 0:
            print("\nErreur : aucun nombre !")
            return

        print(f"\nMoyenne : {moyenne(liste)}")
        print(f"Médiane : {mediane(liste)}")
        print(f"Écart-type : {ecart_type(liste)}")
        print(f"Min : {minimum(liste)}")
        print(f"Max : {maximum(liste)}")

        operation = f"Stats de {liste}: moy={moyenne(liste):.2f}, med={mediane(liste):.2f}"
        historique.append(operation)

    except ValueError:
        print("\nErreur : format invalide !")

def menu_nombres_premiers(historique):
    print("\n--- NOMBRES PREMIERS ET PGCD/PPCM ---")
    print("1. Test de primalité")
    print("2. Décomposition en facteurs premiers")
    print("3. PGCD")
    print("4. PPCM")
    print("5. Retour")

    choix = input("Choix : ")

    if choix == '1':
        n = int(demander_nombre("n : "))

        if est_premier(n):
            print(f"\n{n} est premier")
            historique.append(f"{n} est premier")
        else:
            print(f"\n{n} n'est pas premier")
            historique.append(f"{n} n'est pas premier")

    elif choix == '2':
        n = int(demander_nombre("n : "))
        facteurs = decomposition_premiers(n)

        if len(facteurs) == 0:
            print(f"\n{n} ne peut pas être décomposé")
        else:
            print(f"\nDécomposition de {n} : {' × '.join(map(str, facteurs))}")
            operation = f"{n} = {' × '.join(map(str, facteurs))}"
            historique.append(operation)

    elif choix == '3':
        a = demander_nombre("Premier nombre : ")
        b = demander_nombre("Deuxième nombre : ")
        resultat = pgcd(a, b)

        operation = f"PGCD({int(a)}, {int(b)}) = {resultat}"
        print(f"\nRésultat : {operation}")
        historique.append(operation)

    elif choix == '4':
        a = demander_nombre("Premier nombre : ")
        b = demander_nombre("Deuxième nombre : ")
        resultat = ppcm(a, b)

        operation = f"PPCM({int(a)}, {int(b)}) = {resultat}"
        print(f"\nRésultat : {operation}")
        historique.append(operation)

def main():
    historique = []

    print("="*60)
    print("Bienvenue dans ma calculatrice scientifique !")
    print("Tous les calculs sont codés à la main (pas de librairie)")
    print("="*60)

    while True:
        afficher_menu()
        choix = input("Choix : ")

        if choix == '1':
            print("\nOpérations : +, -, *, /, ** (puissance), % (modulo)")

            nombre1 = demander_nombre("Premier nombre : ")
            operateur = input("Opérateur : ")
            nombre2 = demander_nombre("Deuxième nombre : ")

            operateur_original = operateur
            if operateur == 'x':
                operateur = '*'
            elif operateur == '÷':
                operateur = '/'
            elif operateur == '^':
                operateur = '**'

            resultat = calculer(nombre1, nombre2, operateur)

            if resultat is None:
                if operateur not in ['+', '-', '*', '/', '**', '%']:
                    print(f"\nErreur : opérateur '{operateur_original}' inconnu !")
                else:
                    print("\nErreur : division par zéro !")
            else:
                operation = f"{nombre1} {operateur} {nombre2} = {resultat}"
                print(f"\nRésultat : {operation}")
                historique.append(operation)

        elif choix == '2':
            menu_puissances_racines(historique)

        elif choix == '3':
            menu_trigonometrie(historique)

        elif choix == '4':
            menu_trigonometrie_inverse(historique)

        elif choix == '5':
            menu_logarithmes(historique)

        elif choix == '6':
            menu_factorielle_combinatoire(historique)

        elif choix == '7':
            menu_statistiques(historique)

        elif choix == '8':
            menu_nombres_premiers(historique)

        elif choix == '9':
            afficher_historique(historique)

        elif choix == '10':
            if len(historique) > 0:
                confirmation = input("\nEffacer l'historique ? (o/n) : ")
                if confirmation.lower() == 'o' or confirmation.lower() == 'oui':
                    historique.clear()
                    print("Historique effacé")
                else:
                    print("Annulé")
            else:
                print("\nHistorique déjà vide")

        elif choix == '11':
            print("\n" + "="*60)
            print("Merci d'avoir utilisé ma calculatrice !")
            print("="*60)
            break

        elif choix == '12':
            menu_graphique_original(historique)

        else:
            print("\nErreur : choix invalide")

if __name__ == "__main__":
    main()
