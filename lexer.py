import re

# Definição dos tokens
TOKEN_SPEC = [
    ('COMMENT',    r'#.*'),
    ('TYPE',       r'\b(int|float|string)\b'),
    ('KEYWORD',    r'\b(if|else|switch|case|default|while|for|break|continue|procedure|function|return)\b'),
    ('LOGIC',      r'\b(and|or|not)\b'),
    ('NUMBER',     r'\d+(\.\d+)?'),
    ('STRING',     r'"[^"]*"'),
    ('ID',         r'[a-zA-Z_]\w*'),
    ('OP_COMP',    r'[<>!=]=|[<>]|=='),
    ('OP_ARIT',    r'[+\-*/%]'),
    ('ASSIGN',     r'='),
    ('PONTO_V',    r';'),
    ('COLON',      r':'),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('COMMA',      r','),
    ('NEWLINE',    r'\n'),
    ('SKIP',       r'[ \t]+'),
    ('MISMATCH',   r'.'),
]

class RoboticaLexer:
    def __init__(self):
        self.symbol_table = []
        self.tokens_found = []

    def tokenize(self, code):
        line_num = 1
        line_start = 0
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
        
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start

            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                print(f"ERRO LÉXICO: Símbolo '{value}' desconhecido na linha {line_num}")
                continue

            self.tokens_found.append((kind, value))
            self.symbol_table.append({
                "Lexema": value, "Token": kind, "Linha": line_num, "Coluna": column
            })
        return self.tokens_found

    # Geração do HTML
    def export_html(self, filename="tabela_simbolos.html"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("<html><body><h2>Tabela de Símbolos - RoboticaLang</h2><table border='1'>")
            f.write("<tr><th>Lexema</th><th>Token</th><th>Linha</th><th>Coluna</th></tr>")
            for e in self.symbol_table:
                f.write(f"<tr><td>{e['Lexema']}</td><td>{e['Token']}</td><td>{e['Linha']}</td><td>{e['Coluna']}</td></tr>")
            f.write("</table></body></html>")