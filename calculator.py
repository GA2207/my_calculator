HISTORY_FILE = "history.txt"
OPS = {
    "+": (1, "L"),
    "-": (1, "L"),
    "*": (2, "L"),
    "/": (2, "L"),
    "%": (2, "L"),
    "^": (3, "R"),
}
def save_history(line: str) -> None:
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def read_history() -> str:
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def clear_history() -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("")

def tokenize(expr: str) -> list[str]:
    """Découpe l'expression en nombres/opérateurs. Supporte décimaux et espaces."""
    tokens = []
    i = 0
    expr = expr.replace(" ", "")

    while i < len(expr):
        ch = expr[i]
                # parenthèses
        if ch in ("(", ")"):
            tokens.append(ch)
            i += 1
            continue

        # opérateur
        if ch in OPS:
            # gérer le moins unaire: "-3" ou "2*-3"
            if ch == "-" and (not tokens or tokens[-1] in OPS):
                j = i + 1
                num = "-"
                dot = 0
                while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                    if expr[j] == ".":
                        dot += 1
                        if dot > 1:
                            raise ValueError("Nombre invalide (trop de points).")
                    num += expr[j]
                    j += 1
                if num == "-":
                    raise ValueError("Nombre négatif invalide.")
                tokens.append(num)
                i = j
                continue

            tokens.append(ch)
            i += 1
            continue

        # nombre
        if ch.isdigit() or ch == ".":
            j = i
            dot = 0
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                if expr[j] == ".":
                    dot += 1
                    if dot > 1:
                        raise ValueError("Nombre invalide (trop de points).")
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue

        raise ValueError(f"Caractère invalide: '{ch}'")

    return tokens

def to_rpn(tokens: list[str]) -> list[str]:
    """
    Transforme tokens en RPN (notation postfixée) pour gérer priorités + parenthèses.
    """
    output: list[str] = []
    stack: list[str] = []

    for tok in tokens:
        # opérateur
        if tok in OPS:
            prec_tok, assoc_tok = OPS[tok]

            while stack and stack[-1] in OPS:
                prec_top, _assoc_top = OPS[stack[-1]]

                # assoc gauche: on sort les ops de priorité >=
                # assoc droite: on sort les ops de priorité >
                if (assoc_tok == "L" and prec_top >= prec_tok) or (assoc_tok == "R" and prec_top > prec_tok):
                    output.append(stack.pop())
                else:
                    break

            stack.append(tok)

        # parenthèse ouvrante
        elif tok == "(":
            stack.append(tok)

        # parenthèse fermante
        elif tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Parenthèses mal fermées.")
            stack.pop()  # enlève "("

        # nombre
        else:
            output.append(tok)

    # vider la pile
    while stack:
        if stack[-1] in ("(", ")"):
            raise ValueError("Parenthèses mal fermées.")
        output.append(stack.pop())

    return output


def eval_rpn(rpn: list[str]) -> float:
    """
    Calcule une expression en RPN.
    Exemple RPN: 2 3 4 * +  => 2 + (3*4)
    """
    stack: list[float] = []

    for tok in rpn:
        if tok in OPS:
            if len(stack) < 2:
                raise ValueError("Expression invalide (opérateur mal placé).")
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_op(a, tok, b))
        else:
            try:
                stack.append(float(tok))
            except ValueError:
                raise ValueError(f"Nombre invalide: '{tok}'") from None

    if len(stack) != 1:
        raise ValueError("Expression invalide.")
    return stack[0]

def apply_op(a: float, op: str, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division par zéro interdite.")
        return a / b
    if op == "%":
        if b == 0:
            raise ZeroDivisionError("Modulo par zéro interdit.")
        return a % b
    if op == "^":
        return a ** b
    raise ValueError(f"Opérateur inconnu: {op}")

def calculate(expr: str) -> float:
    tokens = tokenize(expr)
    if len(tokens) < 3:
        raise ValueError("Veuillez saisir au moins 2 nombres et 1 opérateur.")
    rpn = to_rpn(tokens)
    return eval_rpn(rpn)

def menu() -> None:
    while True:
        print("\n=== Calculatrice ===")
        print("1) Calculer une expression (ex: 2+3*4-6/2)")
        print("2) Voir l'historique")
        print("3) Effacer l'historique")
        print("4) Quitter")

        choice = input("Choix: ").strip()

        if choice == "1":
            expr = input("Expression: ").strip()
            try:
                res = calculate(expr)
                print(f"Résultat: {res}")
                save_history(f"{expr} = {res}")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "2":
            h = read_history()
            print("\n--- Historique ---")
            print(h if h else "Historique vide.")

        elif choice == "3":
            clear_history()
            print("Historique réinitialisé.")

        elif choice == "4":
            print("Bye.")
            break

        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
