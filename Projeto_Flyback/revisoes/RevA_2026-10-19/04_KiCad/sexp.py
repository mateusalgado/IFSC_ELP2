"""Parser/serializer minimo de s-expressions do KiCad (kicad_sym, kicad_sch, kicad_mod)."""
import re
from pathlib import Path

TOKEN = re.compile(r'''\s*(?:(\()|(\))|("(?:[^"\\]|\\.)*")|([^\s()"]+))''', re.S)


def parse(text):
    pos = 0
    stack = [[]]
    n = len(text)
    while pos < n:
        m = TOKEN.match(text, pos)
        if not m:
            if text[pos:].strip() == "":
                break
            raise ValueError(f"token invalido em {pos}: {text[pos:pos+30]!r}")
        pos = m.end()
        if m.group(1):
            stack.append([])
        elif m.group(2):
            lst = stack.pop()
            stack[-1].append(lst)
        elif m.group(3):
            stack[-1].append(QStr(m.group(3)[1:-1].replace('\\"', '"')))
        elif m.group(4):
            stack[-1].append(m.group(4))
    return stack[0]


class QStr(str):
    """string que deve ser serializada entre aspas"""
    pass


def dumps(node, indent=0):
    if isinstance(node, QStr):
        return '"' + node.replace('"', '\\"') + '"'
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float)):
        return fmtnum(node)
    pad = "  " * indent
    if not node:
        return "()"
    head = node[0]
    simple = all(not isinstance(x, list) for x in node)
    if simple:
        return "(" + " ".join(dumps(x) for x in node) + ")"
    out = "(" + dumps(head)
    inline = []
    i = 1
    while i < len(node) and not isinstance(node[i], list):
        inline.append(dumps(node[i])); i += 1
    if inline:
        out += " " + " ".join(inline)
    for x in node[i:]:
        out += "\n" + pad + "  " + dumps(x, indent + 1)
    out += "\n" + pad + ")"
    return out


def fmtnum(x):
    if isinstance(x, int):
        return str(x)
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def find(node, key):
    """primeiro filho cujo head == key"""
    for x in node:
        if isinstance(x, list) and x and x[0] == key:
            return x
    return None


def find_all(node, key):
    return [x for x in node if isinstance(x, list) and x and x[0] == key]


def load_symbol(lib_path, name):
    """retorna o no (symbol "name" ...) de um .kicad_sym"""
    txt = Path(lib_path).read_text(encoding="utf-8")
    # localiza o bloco pelo balanceamento de parenteses (rapido para libs grandes)
    key = f'(symbol "{name}"'
    i = txt.find(key)
    if i < 0:
        raise KeyError(name)
    depth = 0; j = i
    while True:
        c = txt[j]
        if c == '"':
            j = txt.find('"', j + 1) + 1
            while txt[j - 2] == "\\":
                j = txt.find('"', j) + 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
        j += 1
    return parse(txt[i:j + 1])[0]


def symbol_pins(sym):
    """lista de (numero, nome, x, y, angulo, comprimento) de todas as unidades/estilos"""
    pins = []
    for unit in find_all(sym, "symbol"):
        for p in find_all(unit, "pin"):
            at = find(p, "at"); num = find(p, "number"); nm = find(p, "name"); ln = find(p, "length")
            pins.append(dict(number=str(num[1]), name=str(nm[1]), x=float(at[1]), y=float(at[2]), rot=float(at[3]) if len(at) > 3 else 0.0,
                             length=float(ln[1]) if ln else 2.54, unit=str(unit[1])))
    return pins


if __name__ == "__main__":
    import sys
    lib, name = sys.argv[1], sys.argv[2]
    s = load_symbol(lib, name)
    ext = find(s, "extends")
    print("extends:", ext[1] if ext else None)
    for p in symbol_pins(s):
        print(p)
