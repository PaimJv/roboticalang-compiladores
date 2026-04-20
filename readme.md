# RoboticaLang - Analisador Léxico

Este projeto refere-se à implementação da primeira etapa de um compilador (Analisador Léxico) para a linguagem **RoboticaLang**, desenvolvida como parte do TDE (Trabalho Discente Efetivo) do curso de Engenharia da Computação - Centro Universitário Nobre (UNIFAN).

## Sobre a Linguagem

A **RoboticaLang** é uma linguagem procedural com foco em clareza e controle de fluxos lógicos, utilizando sintaxe em inglês e estruturação por identação.

### Requisitos Implementados (1 ao 15):

1. **Palavras-chave:** Suporte a tipos (`int`, `float`, `string`), fluxos (`if`, `else`, `switch`, `case`) e rotinas (`procedure`, `function`).
2. **Expressões:** Reconhecimento de parênteses em expressões matemáticas.
3. **Operadores Aritméticos:** `+`, `-`, `*`, `/`, `%`.
4. **Operadores Lógicos:** `and`, `or`, `not`.
5. **Operadores de Comparação:** `>`, `<`, `>=`, `<=`, `!=`, `==`.
6. **Tipos de Dados:** Diferenciação entre inteiros, decimais e strings.
7. **Atribuição:** Uso do símbolo `=` e terminador `;`.
8. **Controle de Fluxo:** Estruturas `if/else` e `switch/case`.
9. **Loops:** Suporte a `while` e `for`.
10. **Rotinas:** Definição de `procedure` (sem retorno) e `function` (com retorno).
11. **Comentários:** Linhas iniciadas com `#` são ignoradas pelo léxico.
12. **Controle de Loop:** Implementação dos tokens `break` e `continue`.

---

## Estrutura do Projeto

* `lexer.py`: Contém a classe `RoboticaLexer`, responsável por converter o texto fonte em tokens via Expressões Regulares (Regex).
* `main.py`: Script principal que carrega o código fonte, executa o léxico e gera os outputs.
* `programa_teste.robotica`: Arquivo de exemplo contendo todas as estruturas da linguagem.
* `tabela_simbolos.html`: Arquivo gerado automaticamente contendo a Tabela de Símbolos formatada.

---

## Como Executar

### Pré-requisitos

* Python 3.x instalado.

### Passo a Passo

1. Certifique-se de que os arquivos `lexer.py`, `main.py` e `programa_teste.robotica` estão na mesma pasta.
2. Abra o terminal ou prompt de comando nesta pasta.
3. Execute o comando:
   ```bash
   python main.py
   ```
4. O terminal exibirá a sequência de tokens gerada.
5. Abra o arquivo `tabela_simbolos.html` em qualquer navegador para visualizar a tabela detalhada.

---

## Detalhes da Implementação

O analisador léxico utiliza a técnica de **Scanning por Regex**. Cada token é definido por um padrão específico. Caso o script encontre um caractere que não pertença a nenhum padrão definido, ele dispara um **Erro Léxico**, indicando a linha e a posição exata do problema, conforme exigido no TDE.

---

**Desenvolvedores:** Davi Leão, Ítalo Andrade, João Victor Paim e Lucas Nascimento
**Instituição:** UNIFAN - Centro Universitário Nobre
**Disciplina:** Compiladores
