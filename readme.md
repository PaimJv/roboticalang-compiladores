# RoboticaLang - Analisador Léxico e Sintático

Este projeto refere-se à implementação das duas primeiras etapas fundamentais de um compilador (Analisador Léxico e Analisador Sintático) para a linguagem **RoboticaLang**, desenvolvida como parte do TDE (Trabalho Discente Efetivo) da disciplina de Compiladores do curso de Engenharia da Computação - Centro Universitário Nobre (UNIFAN).

## Sobre a Linguagem

A **RoboticaLang** é uma linguagem procedural com foco em clareza, legibilidade e controle de fluxos lógicos de hardware, utilizando palavras-chave em inglês e estruturação de blocos definida por `:` e identação de código.

### Requisitos e Funcionalidades Implementadas (1 ao 15):

1. **Palavras-chave:** Suporte completo a tipos de dados (`int`, `float`, `string`), fluxos condicionais (`if`, `else`, `switch`, `case`, `default`) e sub-rotinas (`procedure`, `function`).
2. **Expressões Matemáticas e Lógicas:** Reconhecimento, agrupamento e precedência de parênteses em expressões simples ou complexas.
3. **Operadores Aritméticos:** Suporte a todas as operações essenciais: `+` (soma), `-` (subtração), `*` (multiplicação), `/` (divisão) e `%` (resto da divisão).
4. **Operadores Lógicos:** Expressões condicionais utilizando `and` (E lógico), `or` (OU lógico) e `not` (negação).
5. **Operadores de Comparação:** `>`, `<`, `>=`, `<=`, `!=` (diferente de) e `==` (igual a).
6. **Tipos de Dados:** Identificação e separação rigorosa entre números inteiros, números de ponto flutuante (decimais) e cadeias de caracteres (strings entre aspas).
7. **Regras de Declaração e Atribuição:** Validação de inicialização de variáveis por tipo e atribuições utilizando o símbolo `=` casado com o terminador obrigatório `;`.
8. **Estruturas de Controle de Fluxo:** Implementação sintática de blocos condicionais encadeados (`if/else`).
9. **Estrutura de Loop:** Suporte a laços de repetição estruturados utilizando a instrução `while`.
10. **Controle Avançado de Loop:** Reconhecimento dos comandos de interrupção e continuidade `break` e `continue` de forma sequencial dentro de laços.
11. **Múltipla Escolha:** Implementação completa da estrutura seletiva `switch / case / default`.
12. **Sub-rotinas Estruturadas:** Suporte à criação de `procedure` (procedimentos sem retorno) e `function` (funções com retorno explícito via comando `return`), ambas permitindo a passagem de múltiplos parâmetros.
13. **Comentários no Código:** Linhas iniciadas com o caractere `#` são inteiramente desconsideradas pelo analisador léxico.
14. **Expressões Condicionais Compostas:** Permissão para utilizar múltiplos operadores relacionais e lógicos acoplados na mesma sentença de fluxo.

---

## Estrutura do Projeto

O compilador está modularizado nos seguintes arquivos:

* `lexer.py`: Responsável pela análise léxica. Realiza o *scanning* do código-fonte através de Expressões Regulares (Regex), gerando a sequência ordenada de tokens e populando a tabela de símbolos interna.
* `parser_robotica.py`: Responsável pela análise sintática. Implementa um algoritmo de **Descida Recursiva** que valida a árvore gramatical e constrói a estrutura hierárquica do programa.
* `main.py`: Script unificado de orquestração. Gerencia o fluxo de compilação, exibe os rastreamentos no console, gerencia as pastas e aciona as exportações.

### Diretório de Saída (`/arquivos gerados`)

Para manter o projeto organizado, o script cria automaticamente uma subpasta chamada `arquivos gerados/` contendo os artefatos exigidos no TDE:

* `tabela_simbolos.html`: Tabela de símbolos detalhada (contendo Lexema, Token, Linha e Coluna) exportada em formato de página web para conferência visual.
* `ast.json`: A Árvore Sintática Abstrata (AST) do programa gerada com sucesso e serializada estruturalmente em formato JSON estruturado.

---

## Como Executar

### Pré-requisitos

* Python 3.x instalado no sistema operacional.

### Passo a Passo

1. Certifique-se de que os arquivos `lexer.py`, `parser_robotica.py` e `main.py` estão localizados no mesmo diretório.
2. Abra o terminal de comandos (ou Prompt de Comando/PowerShell no Windows) dentro desta pasta.
3. Inicie o processo executando:

   ```bash
   python main.py
   ```


4. O console do terminal detalhará o andamento passo a passo da compilação e imprimirá a sequência linear de tokens.
5. Abra a subpasta `/arquivos gerados` gerada na raiz do projeto para inspecionar os relatórios finais (`tabela_simbolos.html` e `ast.json`).


## Tratamento de Erros e Validações

O compilador foi projetado para reportar de forma clara qualquer violação às regras da linguagem conforme estabelecido no escopo acadêmico:

* **Erros Léxicos:** Símbolos desconhecidos, caracteres inválidos fora de strings ou lexemas malformados disparam um alerta imediato no terminal apontando o caractere faltante e o número da linha (`MISMATCH`).
* **Erros Sintáticos:** Caso a estrutura não obedeça às produções gramaticais da linguagem, o Parser interrompe a compilação de forma segura e aponta o erro estrutural exato. Exemplos validados:
  * *Ausência de ponto e vírgula:* Exibe `Erro Sintático na linha X: Esperado token 'PONTO_V'`.
  * *Ausência de delimitadores em condições:* Exibe `Erro Sintático na linha X: Esperado token 'LPAREN' (parênteses após o if/while)`.



**Desenvolvedores:** Davi Leão, Ítalo Andrade, João Victor Paim e Lucas Nascimento

**Instituição:** UNIFAN - Centro Universitário Nobre

**Disciplina:** Compiladores