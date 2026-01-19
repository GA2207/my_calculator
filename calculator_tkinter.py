import customtkinter as ctk  # Librairie pour faire une interface graphique moderne (basée sur Tkinter)
from tkinter import messagebox  # Boîtes de dialogue (erreur, confirmation, etc.)
import matplotlib.pyplot as plt  # Pour tracer des graphiques
import os  # Pour gérer les fichiers (vérifier si un fichier existe, supprimer, etc.)

# THEME / COULEURS
ctk.set_appearance_mode("light")          # Mode clair
ctk.set_default_color_theme("blue")       # Thème de base (couleurs des widgets CTk)

# Palette de couleurs (pour harmoniser l'interface)
COL_BG = "#F6EFE6"          # Couleur de fond principale
COL_CARD = "#EFE3D3"        # Couleur des "cartes" (blocs)
COL_TEXT = "#1F1F1F"        # Couleur du texte principal
COL_ACCENT = "#2F5D50"      # Couleur accent (boutons, titres)
COL_GOLD = "#B68D40"        # Petite barre dorée décorative
COL_BTN = "#FFFFFF"         # Couleur bouton standard
COL_BTN_OP = "#E7F0ED"      # Couleur bouton "opérations"
COL_BTN_DANGER = "#F3D9D9"  # Couleur bouton "danger" (effacer historique)

HISTORY_FILE = "history.txt"  # Fichier où on stocke l'historique des calculs

# OUTILS HISTORIQUE
def save_history(line: str) -> None:
    """Ajoute une ligne dans le fichier d'historique."""
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def read_history() -> str:
    """Lit tout l'historique et renvoie une chaîne. Si le fichier n'existe pas, renvoie vide."""
    if not os.path.exists(HISTORY_FILE):
        return ""
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def clear_history() -> None:
    """Supprime le fichier d'historique (donc efface tout)."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# FONCTIONS MATH (calculs)

def demander_nombre_console(message):
    """
    Ancienne fonction console : demande un nombre via input().
    Gardée si tu veux réutiliser en mode console, mais l'interface graphique n'en a pas besoin.
    """
    while True:
        try:
            entree = input(message)
            # Support de la virgule (ex: 3,14)
            if '.' in entree or ',' in entree:
                entree = entree.replace(',', '.')
                return float(entree)
            else:
                return int(entree)
        except ValueError:
            print("Erreur : entre un nombre valide stp !")

# Opérations de base
def additionner(a, b): return a + b          # Addition
def soustraire(a, b): return a - b           # Soustraction
def multiplier(a, b): return a * b           # Multiplication

def diviser(a, b):
    """Division avec protection contre la division par zéro."""
    if b == 0: 
        return None
    return a / b

def puissance(a, b):
    """
    Puissance "manuel" : calcule a^b sans utiliser **.
    - gère b=0
    - gère b négatif (retourne 1/(a^|b|)
    """
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
    """Modulo "manuel" avec protection b=0."""
    if b == 0: 
        return None
    quotient = int(a / b)
    reste = a - (quotient * b)
    return reste

def factorielle(n):
    """Factorielle n! (uniquement pour n >= 0)."""
    if n < 0: 
        return None
    if n == 0 or n == 1: 
        return 1
    resultat = 1
    for i in range(2, int(n) + 1):
        resultat *= i
    return resultat

def racine_carree(n, precision=0.000001):
    """
    Racine carrée via méthode de Newton.
    - retourne None si n < 0
    """
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
    """
    Racine n-ième via Newton.
    - n=0 => impossible
    - nombre négatif avec n pair => impossible
    - gère les racines impaires des nombres négatifs
    """
    if n == 0: 
        return None
    if nombre < 0 and n % 2 == 0: 
        return None
    if nombre == 0: 
        return 0

    # Si nombre est négatif, on calcule sur la valeur positive et on remet le signe à la fin
    negatif = False
    if nombre < 0:
        negatif = True
        nombre = -nombre

    x = nombre
    for _ in range(100):  # limite de sécurité pour éviter une boucle infinie
        x_nouveau = ((n - 1) * x + nombre / puissance(x, n - 1)) / n
        if abs(x_nouveau - x) < precision:
            return -x_nouveau if negatif else x_nouveau
        x = x_nouveau
    return -x if negatif else x

def valeur_absolue(n):
    """Retourne la valeur absolue."""
    return -n if n < 0 else n

def logarithme_naturel(x, precision=0.000001):
    """
    ln(x) approx :
    - x doit être > 0
    - utilise une série quand x est proche de 1, sinon réduit x par des divisions par e
    """
    if x <= 0: 
        return None
    # Cas "proche de 1" : série plus stable
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
    # Cas x grand : on ramène x vers 2 en divisant par e
    elif x >= 2:
        compteur = 0
        E = 2.718281828459045
        while x > 2:
            x /= E
            compteur += 1
        return compteur + logarithme_naturel(x, precision)
    # Cas x petit : ln(x) = -ln(1/x)
    else:
        return -logarithme_naturel(1 / x, precision)

def logarithme_base(x, base):
    """log_base(x) = ln(x) / ln(base), avec vérifications."""
    if x <= 0 or base <= 0 or base == 1:
        return None
    ln_x = logarithme_naturel(x)
    ln_base = logarithme_naturel(base)
    if ln_x is None or ln_base is None:
        return None
    return ln_x / ln_base

def exponentielle(x, precision=0.000001):
    """
    exp(x) via série de Taylor :
    e^x = 1 + x + x^2/2! + ...
    """
    resultat = 1
    terme = 1
    for n in range(1, 100):
        terme *= x / n
        resultat += terme
        if abs(terme) < precision:
            break
    return resultat

def degres_vers_radians(degres):
    """Conversion degrés -> radians."""
    PI = 3.14159265358979323846
    return degres * PI / 180

def sinus(x, en_degres=False):
    """
    sinus via série de Taylor.
    - possibilité de donner l'angle en degrés
    - réduction de l'angle pour améliorer la précision
    """
    if en_degres:
        x = degres_vers_radians(x)
    PI = 3.14159265358979323846
    deux_pi = 2 * PI
    while x > PI:
        x -= deux_pi
    while x < -PI:
        x += deux_pi
    terme = x
    somme = terme
    for n in range(1, 20):
        terme *= -x * x / ((2 * n) * (2 * n + 1))
        somme += terme
    return somme

def cosinus(x, en_degres=False):
    """
    cosinus via série de Taylor.
    - possibilité de donner l'angle en degrés
    - réduction de l'angle pour améliorer la précision
    """
    if en_degres:
        x = degres_vers_radians(x)
    PI = 3.14159265358979323846
    deux_pi = 2 * PI
    while x > PI:
        x -= deux_pi
    while x < -PI:
        x += deux_pi
    terme = 1
    somme = terme
    for n in range(1, 20):
        terme *= -x * x / ((2 * n - 1) * (2 * n))
        somme += terme
    return somme

def tangente(x, en_degres=False):
    """
    tan(x) = sin(x) / cos(x)
    - si cos(x) ~ 0 => tangente indéfinie => None
    """
    cos_x = cosinus(x, en_degres)
    if abs(cos_x) < 0.0000001:
        return None
    return sinus(x, en_degres) / cos_x

def arcsinus(x, precision=0.000001):
    """
    arcsin(x) approx (série).
    - x doit être entre -1 et 1
    """
    if x < -1 or x > 1: 
        return None
    PI = 3.14159265358979323846
    if x == 1: 
        return PI / 2
    if x == -1: 
        return -PI / 2
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
    """arccos(x) = PI/2 - arcsin(x)."""
    arcsin_x = arcsinus(x)
    if arcsin_x is None:
        return None
    PI = 3.14159265358979323846
    return PI / 2 - arcsin_x

def arctangente(x, precision=0.000001):
    """
    arctan(x) approx (série).
    - gère les grands x via identités pour améliorer la stabilité.
    """
    PI = 3.14159265358979323846
    if x > 1:
        return PI / 2 - arctangente(1 / x, precision)
    if x < -1:
        return -PI / 2 - arctangente(1 / x, precision)
    resultat = 0
    terme = x
    x_carre = x * x
    for n in range(50):
        resultat += terme / (2 * n + 1)
        terme *= -x_carre
        if abs(terme / (2 * n + 3)) < precision:
            break
    return resultat

# STATS
def moyenne(liste):
    """Moyenne d'une liste (None si liste vide)."""
    if len(liste) == 0: 
        return None
    s = 0
    for n in liste:
        s += n
    return s / len(liste)

def mediane(liste):
    """
    Médiane :
    - trie la liste (tri à bulles ici)
    - renvoie le milieu (ou la moyenne des deux milieux si pair)
    """
    if len(liste) == 0: 
        return None
    a = liste.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    if n % 2 == 0:
        return (a[n // 2 - 1] + a[n // 2]) / 2
    return a[n // 2]

def ecart_type(liste):
    """Écart-type (population) : sqrt(variance)."""
    if len(liste) == 0: 
        return None
    moy = moyenne(liste)
    sc = 0
    for n in liste:
        d = n - moy
        sc += d * d
    variance = sc / len(liste)
    return racine_carree(variance)

def minimum(liste):
    """Minimum d'une liste."""
    if len(liste) == 0: 
        return None
    m = liste[0]
    for n in liste:
        if n < m:
            m = n
    return m

def maximum(liste):
    """Maximum d'une liste."""
    if len(liste) == 0: 
        return None
    m = liste[0]
    for n in liste:
        if n > m:
            m = n
    return m

# COMBINATOIRE
def combinaison(n, k):
    """Combinaison C(n,k) (nombre de façons de choisir k éléments parmi n)."""
    if k < 0 or k > n: 
        return None
    if k == 0 or k == n: 
        return 1
    if k > n - k:
        k = n - k  # optimisation
    res = 1
    for i in range(k):
        res *= (n - i)
        res /= (i + 1)
    return int(res)

def arrangement(n, k):
    """Arrangement A(n,k) (nombre de façons d'ordonner k éléments parmi n)."""
    if k < 0 or k > n: 
        return None
    res = 1
    for i in range(n, n - k, -1):
        res *= i
    return int(res)

# NOMBRES PREMIERS / PGCD / PPCM
def est_premier(n):
    """Test si n est premier (méthode simple)."""
    if n < 2: 
        return False
    if n == 2: 
        return True
    if n % 2 == 0: 
        return False
    i = 3
    r = int(racine_carree(n)) + 1
    while i <= r:
        if n % i == 0:
            return False
        i += 2
    return True

def decomposition_premiers(n):
    """Décompose n en facteurs premiers (ex: 12 -> [2,2,3])."""
    if n < 2: 
        return []
    facteurs = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            facteurs.append(d)
            n //= d
        d += 1
    if n > 1:
        facteurs.append(n)
    return facteurs

def pgcd(a, b):
    """PGCD via l'algorithme d'Euclide."""
    a, b = int(abs(a)), int(abs(b))
    while b != 0:
        a, b = b, a % b
    return a

def ppcm(a, b):
    """PPCM = |a*b| / PGCD(a,b) (si a ou b vaut 0 => 0)."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // pgcd(a, b)

# TRACEUR : petit parseur "manuel"
# Objectif : permettre des expressions du style "2x+1", "2(x+1)", "(x+1)(x-1)" etc.
def calculer_point_graphique(expression, x_val):
    """
    Calcule f(x) pour une expression entrée par l'utilisateur.
    - remplace x par la valeur x_val
    - gère quelques fonctions (sinus, cosinus, etc.)
    - gère la multiplication implicite (ex: 2(x+1))
    """
    exp = expression.replace(" ", "").lower()
    exp = exp.replace("**", "^")                 # uniformise la puissance
    exp = exp.replace("x", f"({x_val})")         # remplace x par la valeur

    # multiplication implicite : ")(" devient ")*("
    exp = exp.replace(")(", ")*(")

    # ajoute "*" quand on a: chiffre suivi de "("  ->  "2(" devient "2*("
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
        """Résout une expression simple sous forme de texte."""
        if not s:
            return 0

        # 1) Résolution des parenthèses, en détectant aussi les fonctions
        while '(' in s:
            debut = s.find('(')

            # On regarde si juste avant la parenthèse, il y a un nom de fonction connu
            nom_func = ""
            for f in ['sinus', 'cosinus', 'tangente', 'racine_carree', 'exponentielle', 'valeur_absolue']:
                if s[:debut].endswith(f):
                    nom_func = f
                    break

            # On cherche la parenthèse fermante correspondante (gestion des niveaux)
            niveau, fin = 0, -1
            for i in range(debut, len(s)):
                if s[i] == '(':
                    niveau += 1
                elif s[i] == ')':
                    niveau -= 1
                if niveau == 0:
                    fin = i
                    break

            # On résout le contenu entre les parenthèses
            res_int = resoudre(s[debut + 1:fin])

            # Si une fonction est détectée, on applique la fonction
            if nom_func:
                if nom_func == 'sinus':
                    val = sinus(res_int)
                elif nom_func == 'cosinus':
                    val = cosinus(res_int)
                elif nom_func == 'tangente':
                    val = tangente(res_int)
                    if val is None:
                        return 0  # évite crash si tangente indéfinie
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

                # Remplace "fonction(...)" par la valeur calculée
                s = s[:debut - len(nom_func)] + str(val) + s[fin + 1:]
            else:
                # Parenthèses simples : "(...)" devient juste "valeur"
                s = s[:debut] + str(res_int) + s[fin + 1:]

        # 2) Gestion + et - (en partant de la droite pour respecter la priorité)
        for i in range(len(s) - 1, -1, -1):
            if s[i] == '+' and i > 0 and s[i - 1] not in '*/^+-':
                return resoudre(s[:i]) + resoudre(s[i + 1:])
            if s[i] == '-' and i > 0 and s[i - 1] not in '*/^+-':
                return resoudre(s[:i]) - resoudre(s[i + 1:])

        # 3) Gestion * et /
        for i in range(len(s) - 1, -1, -1):
            if s[i] == '*':
                return resoudre(s[:i]) * resoudre(s[i + 1:])
            if s[i] == '/':
                d = resoudre(s[i + 1:])
                return resoudre(s[:i]) / d if d != 0 else 0

        # 4) Gestion puissance ^
        if '^' in s:
            b, e = s.split('^', 1)
            return puissance(resoudre(b), resoudre(e))

        # 5) Nombre final
        try:
            return float(s)
        except:
            return 0

    return resoudre(exp)

# OUTILS GUI : récupération de valeurs via fenêtres
def ask_float(title, prompt):
    """Demande un nombre (float) à l'utilisateur via une boîte de dialogue."""
    dlg = ctk.CTkInputDialog(title=title, text=prompt)
    s = dlg.get_input()
    if s is None:
        return None
    s = s.strip().replace(",", ".")
    if s == "":
        return None
    try:
        return float(s)
    except:
        return None

def ask_int(title, prompt):
    """Demande un entier (utilise ask_float puis convertit en int)."""
    v = ask_float(title, prompt)
    if v is None:
        return None
    return int(v)

def ask_text(title, prompt):
    """Demande un texte (string) à l'utilisateur."""
    dlg = ctk.CTkInputDialog(title=title, text=prompt)
    s = dlg.get_input()
    if s is None:
        return None
    return s.strip()

# APPLICATION CTk : 1 bouton = 1 fonctionnalité
class ScientificTravelCalc(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Paramètres de la fenêtre principale
        self.title("Calculatrice Scientifique (GUI) ✈️")
        self.geometry("520x820")       # Taille fixe
        self.resizable(False, False)   # Empêche le redimensionnement
        self.configure(fg_color=COL_BG)

        # -------- HEADER (haut de page) --------
        header = ctk.CTkFrame(self, fg_color=COL_CARD, corner_radius=18)
        header.pack(fill="x", padx=16, pady=(16, 10))

        top = ctk.CTkFrame(header, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(14, 4))

        # Titre de l'application (à gauche)
        ctk.CTkLabel(
            top,
            text="Scientific • Travel Calculator ✈️",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COL_TEXT,
        ).pack(side="left")

        # Petit emoji décoratif (à droite)
        ctk.CTkLabel(
            top,
            text="🧭",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COL_ACCENT,
        ).pack(side="right")

        # Sous-titre explicatif
        ctk.CTkLabel(
            header,
            text="1 bouton = 1 fonctionnalité (sans menus console)",
            font=ctk.CTkFont(size=12),
            text_color=COL_ACCENT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 12))

        # Barre dorée décorative sous le header
        ctk.CTkFrame(self, fg_color=COL_GOLD, height=4, corner_radius=10).pack(
            fill="x", padx=16, pady=(0, 12)
        )

        # -------- Zone résultat / message --------
        self.result_var = ctk.StringVar(value="Prêt.")
        self.result = ctk.CTkLabel(
            self,
            textvariable=self.result_var,
            fg_color="#FFFFFF",
            text_color=COL_TEXT,
            corner_radius=16,
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            padx=12
        )
        self.result.pack(fill="x", padx=16, pady=(0, 12))

        # -------- Carte principale contenant les boutons --------
        card = ctk.CTkFrame(self, fg_color=COL_CARD, corner_radius=18)
        card.pack(fill="x", padx=16, pady=(0, 12))

        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(padx=12, pady=12)

        # Liste des boutons : (texte, fonction appelée, type de style)
        btns = [
            ("Calcul basique", self.ui_basic, "op"),
            ("Puissances / Racines", self.ui_powers, "op"),
            ("Trigonométrie", self.ui_trigo, "op"),
            ("Trigo inverse", self.ui_trigo_inv, "op"),
            ("Log / Exp", self.ui_logs, "op"),
            ("Factorielle / Combinatoire", self.ui_fact_comb, "op"),
            ("Statistiques", self.ui_stats, "op"),
            ("Premiers / PGCD / PPCM", self.ui_primes_pgcd, "op"),
            ("Tracer f(x)", self.ui_plot, "eq"),
            ("Voir historique", self.refresh_history, "act"),
            ("Effacer historique", self.clear_hist, "danger"),
        ]

        # Placement des boutons en grille : 2 colonnes
        r = c = 0
        for label, cmd, kind in btns:
            b = self.make_button(grid, label, kind, cmd)
            b.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            c += 1
            if c == 2:
                c = 0
                r += 1

        # Les colonnes prennent la place disponible
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        # -------- Zone historique (en bas) --------
        hist_card = ctk.CTkFrame(self, fg_color=COL_CARD, corner_radius=18)
        hist_card.pack(fill="both", padx=16, pady=(0, 16), expand=True)

        ctk.CTkLabel(
            hist_card,
            text="🗒️ Historique",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COL_TEXT,
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.history = ctk.CTkTextbox(
            hist_card,
            corner_radius=14,
            fg_color="#FFFFFF",
            text_color=COL_TEXT,
            font=ctk.CTkFont(size=12),
        )
        self.history.pack(fill="both", padx=16, pady=(0, 16), expand=True)
        self.history.configure(state="disabled")  # lecture seule

        # Chargement initial de l'historique au démarrage
        self.refresh_history()

    def make_button(self, parent, text, kind, cmd):
        """
        Fabrique un bouton avec un style différent selon 'kind' :
        - op : boutons d'opérations
        - act : actions (voir historique)
        - danger : action risquée (effacer)
        - eq : action principale (tracer)
        """
        fg = COL_BTN
        text_col = COL_TEXT
        hover = "#EDEDED"

        if kind == "op":
            fg = COL_BTN_OP
            text_col = COL_ACCENT
            hover = "#DCEAE6"
        elif kind == "act":
            fg = COL_BG
            text_col = COL_TEXT
            hover = "#EFE3D3"
        elif kind == "danger":
            fg = COL_BTN_DANGER
            text_col = COL_TEXT
            hover = "#EFC8C8"
        elif kind == "eq":
            fg = COL_ACCENT
            text_col = "#FFFFFF"
            hover = "#264A40"

        return ctk.CTkButton(
            master=parent,
            text=text,
            height=48,
            corner_radius=16,
            fg_color=fg,
            hover_color=hover,
            text_color=text_col,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=cmd,
        )

    def set_result(self, txt):
        """Met à jour la zone résultat (message en haut)."""
        self.result_var.set(txt)

    # ACTIONS UI (1 bouton = 1 action)
    def ui_basic(self):
        """Calcul basique : demande a, opérateur, b, puis calcule."""
        a = ask_float("Calcul basique", "Premier nombre :")
        if a is None: return

        op = ask_text("Calcul basique", "Opérateur (+, -, *, /, ^, %) :")
        if not op: return

        b = ask_float("Calcul basique", "Deuxième nombre :")
        if b is None: return

        # Choix de l'opération selon l'opérateur saisi
        if op == '^':
            res = puissance(a, b)
        elif op == '+':
            res = additionner(a, b)
        elif op == '-':
            res = soustraire(a, b)
        elif op == '*':
            res = multiplier(a, b)
        elif op == '/':
            res = diviser(a, b)
        elif op == '%':
            res = modulo(a, b)
        else:
            messagebox.showerror("Erreur", "Opérateur inconnu.")
            return

        # Cas impossible (division par 0, modulo par 0, etc.)
        if res is None:
            messagebox.showerror("Erreur", "Calcul impossible (ex: division par 0).")
            return

        # Affichage + sauvegarde historique
        line = f"{a} {op} {b} = {res}"
        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_powers(self):
        """Menu racines / valeur absolue."""
        choice = ask_text("Puissances / Racines", "Choix : 1) racine carrée  2) racine n-ième  3) valeur absolue")
        if not choice: return

        if choice == "1":
            n = ask_float("Racine carrée", "Nombre :")
            if n is None: return
            res = racine_carree(n)
            if res is None:
                messagebox.showerror("Erreur", "Impossible (nombre négatif).")
                return
            line = f"√{n} = {res}"

        elif choice == "2":
            x = ask_float("Racine n-ième", "Nombre :")
            if x is None: return
            n = ask_int("Racine n-ième", "Indice n (entier) :")
            if n is None: return
            res = racine_n(x, n)
            if res is None:
                messagebox.showerror("Erreur", "Calcul impossible.")
                return
            line = f"{n}√{x} = {res}"

        elif choice == "3":
            x = ask_float("Valeur absolue", "Nombre :")
            if x is None: return
            res = valeur_absolue(x)
            line = f"|{x}| = {res}"

        else:
            return

        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_trigo(self):
        """Menu trigo : sin / cos / tan."""
        choice = ask_text("Trigonométrie", "Choix : 1) sinus  2) cosinus  3) tangente")
        if not choice: return

        x = ask_float("Trigonométrie", "Angle :")
        if x is None: return

        unit = ask_text("Trigonométrie", "Unité : d (degrés) ou r (radians) ?")
        if not unit: return

        en_degres = (unit.lower() == "d")

        if choice == "1":
            res = sinus(x, en_degres)
            line = f"sin({x}{'°' if en_degres else ' rad'}) = {res}"
        elif choice == "2":
            res = cosinus(x, en_degres)
            line = f"cos({x}{'°' if en_degres else ' rad'}) = {res}"
        elif choice == "3":
            res = tangente(x, en_degres)
            if res is None:
                messagebox.showerror("Erreur", "Tangente indéfinie pour cet angle.")
                return
            line = f"tan({x}{'°' if en_degres else ' rad'}) = {res}"
        else:
            return

        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_trigo_inv(self):
        """Menu trigo inverse : arcsin / arccos / arctan."""
        choice = ask_text("Trigonométrie inverse", "Choix : 1) arcsin  2) arccos  3) arctan")
        if not choice: return

        v = ask_float("Trigonométrie inverse", "Valeur :")
        if v is None: return

        if choice == "1":
            res = arcsinus(v)
            if res is None:
                messagebox.showerror("Erreur", "arcsin : valeur doit être entre -1 et 1.")
                return
            line = f"arcsin({v}) = {res} rad"

        elif choice == "2":
            res = arccosinus(v)
            if res is None:
                messagebox.showerror("Erreur", "arccos : valeur doit être entre -1 et 1.")
                return
            line = f"arccos({v}) = {res} rad"

        elif choice == "3":
            res = arctangente(v)
            line = f"arctan({v}) = {res} rad"

        else:
            return

        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_logs(self):
        """Menu logarithmes et exponentielle."""
        choice = ask_text("Logarithmes / Exponentielle", "Choix : 1) ln(x)  2) log10(x)  3) log_base(x)  4) exp(x)")
        if not choice: return

        if choice == "1":
            x = ask_float("ln(x)", "x :")
            if x is None: return
            res = logarithme_naturel(x)
            if res is None:
                messagebox.showerror("Erreur", "ln existe seulement pour x > 0.")
                return
            line = f"ln({x}) = {res}"

        elif choice == "2":
            x = ask_float("log10(x)", "x :")
            if x is None: return
            res = logarithme_base(x, 10)
            if res is None:
                messagebox.showerror("Erreur", "log10 existe seulement pour x > 0.")
                return
            line = f"log10({x}) = {res}"

        elif choice == "3":
            x = ask_float("log_base(x)", "x :")
            if x is None: return
            b = ask_float("log_base(x)", "Base :")
            if b is None: return
            res = logarithme_base(x, b)
            if res is None:
                messagebox.showerror("Erreur", "Valeurs invalides (x>0, base>0, base≠1).")
                return
            line = f"log_{b}({x}) = {res}"

        elif choice == "4":
            x = ask_float("exp(x)", "x :")
            if x is None: return
            res = exponentielle(x)
            line = f"e^{x} = {res}"

        else:
            return

        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_fact_comb(self):
        """Menu factorielle, combinaison, arrangement."""
        choice = ask_text("Factorielle / Combinatoire", "Choix : 1) n!  2) C(n,k)  3) A(n,k)")
        if not choice: return

        if choice == "1":
            n = ask_int("Factorielle", "n (entier) :")
            if n is None: return
            res = factorielle(n)
            if res is None:
                messagebox.showerror("Erreur", "Factorielle impossible pour n négatif.")
                return
            line = f"{n}! = {res}"

        elif choice == "2":
            n = ask_int("Combinaison", "n :")
            if n is None: return
            k = ask_int("Combinaison", "k :")
            if k is None: return
            res = combinaison(n, k)
            if res is None:
                messagebox.showerror("Erreur", "k doit être entre 0 et n.")
                return
            line = f"C({n},{k}) = {res}"

        elif choice == "3":
            n = ask_int("Arrangement", "n :")
            if n is None: return
            k = ask_int("Arrangement", "k :")
            if k is None: return
            res = arrangement(n, k)
            if res is None:
                messagebox.showerror("Erreur", "k doit être entre 0 et n.")
                return
            line = f"A({n},{k}) = {res}"

        else:
            return

        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_stats(self):
        """Demande une liste de nombres et calcule moyenne, médiane, écart-type, min, max."""
        s = ask_text("Statistiques", "Entre des nombres séparés par des espaces :")
        if not s: return

        # Transformation texte -> liste de nombres
        try:
            vals = [float(x.replace(",", ".")) for x in s.split()]
            if len(vals) == 0:
                raise ValueError()
        except:
            messagebox.showerror("Erreur", "Format invalide.")
            return

        m = moyenne(vals)
        med = mediane(vals)
        et = ecart_type(vals)
        mi = minimum(vals)
        ma = maximum(vals)

        line = f"Stats {vals} | moy={m} med={med} et={et} min={mi} max={ma}"
        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_primes_pgcd(self):
        """Menu nombres premiers / décomposition / PGCD / PPCM."""
        choice = ask_text("Premiers / PGCD / PPCM", "Choix : 1) test premier  2) décomposition  3) PGCD  4) PPCM")
        if not choice: return

        if choice == "1":
            n = ask_int("Test premier", "n :")
            if n is None: return
            res = est_premier(n)
            line = f"{n} est premier" if res else f"{n} n'est pas premier"

        elif choice == "2":
            n = ask_int("Décomposition", "n :")
            if n is None: return
            fac = decomposition_premiers(n)
            line = f"{n} = {' × '.join(map(str, fac))}" if fac else f"{n} ne peut pas être décomposé"

        elif choice == "3":
            a = ask_int("PGCD", "a :")
            if a is None: return
            b = ask_int("PGCD", "b :")
            if b is None: return
            res = pgcd(a, b)
            line = f"PGCD({a},{b}) = {res}"

        elif choice == "4":
            a = ask_int("PPCM", "a :")
            if a is None: return
            b = ask_int("PPCM", "b :")
            if b is None: return
            res = ppcm(a, b)
            line = f"PPCM({a},{b}) = {res}"

        else:
            return

        self.set_result(line)
        save_history(line)
        self.refresh_history()

    def ui_plot(self):
        """Trace f(x) en demandant l'expression et l'intervalle [xmin, xmax]."""
        expr = ask_text("Tracer f(x)", "Expression (ex: 2x+1 ou sinus(x)*2 + x^2) :")
        if not expr:
            return

        xmin = ask_float("Tracer f(x)", "x min :")
        if xmin is None: return
        xmax = ask_float("Tracer f(x)", "x max :")
        if xmax is None: return

        # Vérifications de base
        if xmax == xmin:
            messagebox.showerror("Erreur", "x max doit être différent de x min.")
            return
        if xmax < xmin:
            xmin, xmax = xmax, xmin

        # Calcul de points pour tracer la courbe
        xs, ys = [], []
        pas = (xmax - xmin) / 400  # nombre de points ~400
        x = xmin
        while x <= xmax:
            y = calculer_point_graphique(expr, x)
            xs.append(x)
            ys.append(y)
            x += pas

        # Tracé avec Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(xs, ys, label=f"f(x) = {expr}")
        plt.axhline(0, linewidth=1)  # axe horizontal
        plt.axvline(0, linewidth=1)  # axe vertical
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.title(f"Graphique : {expr}")
        plt.legend()
        plt.show()

        # Sauvegarde dans l'historique
        save_history(f"Graphique : {expr}  (x de {xmin} à {xmax})")
        self.refresh_history()
        self.set_result(f"Graphique tracé : {expr}")

    def refresh_history(self):
        """Recharge et affiche l'historique dans la zone texte."""
        content = read_history()
        self.history.configure(state="normal")
        self.history.delete("1.0", "end")
        self.history.insert("end", content if content else "Historique vide.")
        self.history.configure(state="disabled")

    def clear_hist(self):
        """Demande confirmation, puis efface l'historique."""
        if messagebox.askyesno("Confirmation", "Effacer l'historique ?"):
            clear_history()
            self.refresh_history()
            self.set_result("Historique effacé.")

# LANCEMENT DE L'APP
def main():
    """Point d'entrée : crée l'application et lance la boucle graphique."""
    app = ScientificTravelCalc()
    app.mainloop()

if __name__ == "__main__":
    main()
