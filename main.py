import os
# Arquivo utilizado para geração da tabela de símbolos e análise sintática
from lexer import RoboticaLexer
from parser_robotica import RoboticaParser

def run_compiler():
    source = """
# RoboticaLang
int status = 1;
float speed = 10.5;

function check_system(int s):
    if (s == 1 and speed > 5.0):
        return 1;
    else:
        return 0;

procedure move():
    while (status == 1):
        speed = speed + 1.0;
        if (speed >= 20.0):
            break;

switch (status):
    case 1:
        move();
    default:
        status = 0;
"""

    print("========================================")
    print("      COMPILADOR - ROBOTICALANG         ")
    print("========================================")

    # --- CONFIGURAÇÃO DA PASTA DE SAÍDA ---
    # Pega o caminho absoluto da pasta onde o main.py está salvo
    pasta_do_main = os.path.dirname(os.path.abspath(__file__))
    # Define o caminho da subpasta "arquivos gerados"
    pasta_saida = os.path.join(pasta_do_main, "arquivos gerados")
    
    # Cria a subpasta automaticamente se ela não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Define o caminho completo de destino para cada arquivo
    caminho_html = os.path.join(pasta_saida, "tabela_simbolos.html")
    caminho_json = os.path.join(pasta_saida, "ast.json")
    # --------------------------------------

    # 1. Análise Léxica
    print("\n[FASE 1] Executando Análise Léxica...")
    lexer = RoboticaLexer()
    tokens = lexer.tokenize(source)

    # Exibir sequência de tokens gerada
    print("--- SEQUÊNCIA DE TOKENS GERADA ---")
    for t in tokens:
        print(f"('{t[0]}', '{t[1]}')", end=" ")
    print("\n")
    
    # Salvar arquivo HTML dentro da nova pasta
    lexer.export_html(caminho_html)
    print(f"-> Tabela de símbolos exportada para: {caminho_html}")

    # 2. Análise Sintática
    print("\n[FASE 2] Executando Análise Sintática...")
    
    parser = RoboticaParser(lexer.symbol_table)
    ast = parser.parse()

    if ast:
        print("\n-> Compilação Sintática concluída sem erros!")
        # Salvar arquivo JSON dentro da nova pasta
        parser.export_json(ast, caminho_json)
        print(f"-> AST exportada para: {caminho_json}")
    else:
        print("\n-> Compilação abortada devido a erros sintáticos.")

if __name__ == "__main__":
    run_compiler()