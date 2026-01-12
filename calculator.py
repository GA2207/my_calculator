HISTORY_FILE = "history.txt"
OPS = {"+", "-", "*", "/"}


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
    raise ValueError(f"Opérateur inconnu: {op}")


def eval_with_precedence(tokens: list[str]) -> float:
    """Calcule en respectant * / avant + -."""
    # 1) Pass * /
    out = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in ("*", "/"):
            if not out:
                raise ValueError("Expression invalide.")
            if i + 1 >= len(tokens):
                raise ValueError("Expression invalide.")

            a = float(out.pop())
            b = float(tokens[i + 1])
            out.append(str(apply_op(a, tok, b)))
            i += 2
        else:
            out.append(tok)
            i += 1

    if not out:
        raise ValueError("Expression vide.")
    result = float(out[0])
    i = 1
    while i < len(out):
        op = out[i]
        if op not in ("+", "-"):
            raise ValueError("Expression invalide (opérateur attendu).")
        if i + 1 >= len(out):
            raise ValueError("Expression invalide (nombre manquant).")
        b = float(out[i + 1])
        result = apply_op(result, op, b)
        i += 2

    return result


def calculate(expr: str) -> float:
    tokens = tokenize(expr)
    # validation simple: alternance nombre/op/nombre
    if len(tokens) < 3:
        raise ValueError("Veuillez saisir au moins 2 nombres et 1 opérateur.")
    return eval_with_precedence(tokens)


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
