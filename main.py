# Arquivo utilizado para geração da tabela de símbolos
from lexer import RoboticaLexer

def run_compiler():
    try:
        with open("programa_teste.robotica", "r") as f:
            source = f.read()
    except FileNotFoundError:
        print("Arquivo de teste não encontrado!")
        return

    lexer = RoboticaLexer()
    tokens = lexer.tokenize(source)

    print("\n--- SEQUÊNCIA DE TOKENS GERADA ---")
    for t in tokens:
        print(f"('{t[0]}', '{t[1]}')", end=" ")
    
    lexer.export_html("tabela_simbolos.html")
    print("\n\nSucesso! Tabela de símbolos exportada para 'tabela_simbolos.html'.")

if __name__ == "__main__":
    run_compiler()