import json

class RoboticaParser:
    def __init__(self, symbol_table):
        # Recebe a tabela de símbolos do Lexer porque ela contém o Token, Lexema e Linha exata!
        self.tokens = symbol_table
        self.pos = 0
        self.erros = []

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, expected_token_type, expected_lexema=None):
        tok = self.current_token()
        if not tok:
            raise SyntaxError(f"Erro Sintático: Fim de arquivo inesperado. Esperado '{expected_token_type}'.")
        
        if tok["Token"] == expected_token_type:
            # Validação extra caso precise de uma palavra-chave específica (ex: 'if' em vez de qualquer KEYWORD)
            if expected_lexema and tok["Lexema"] != expected_lexema:
                raise SyntaxError(f"Erro Sintático na linha {tok['Linha']}: Esperado '{expected_lexema}', mas encontrou '{tok['Lexema']}'.")
            self.pos += 1
            return tok
        else:
            raise SyntaxError(f"Erro Sintático na linha {tok['Linha']}: Esperado '{expected_token_type}', mas encontrou '{tok['Token']}' ('{tok['Lexema']}').")

    def parse(self):
        ast = {"type": "Program", "body": []}
        try:
            while self.current_token() is not None:
                stmt = self.parse_statement()
                if stmt:
                    ast["body"].append(stmt)
            return ast
        except SyntaxError as e:
            print(f"\n[FALHA NA COMPILAÇÃO] {e}")
            return None

    def parse_statement(self):
        tok = self.current_token()
        if not tok:
            return None

        # 1. Declaração de Variável (ex: int status = 1;)
        if tok["Token"] == "TYPE":
            type_tok = self.match("TYPE")
            id_tok = self.match("ID")
            self.match("ASSIGN")
            expr = self.parse_expression()
            self.match("PONTO_V")
            return {"type": "VariableDeclaration", "dataType": type_tok["Lexema"], "id": id_tok["Lexema"], "init": expr}

        # 2. Declaração de Função
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "function":
            self.match("KEYWORD", "function")
            id_tok = self.match("ID")
            self.match("LPAREN")
            params = []
            if self.current_token() and self.current_token()["Token"] == "TYPE":
                p_type = self.match("TYPE")
                p_id = self.match("ID")
                params.append({"dataType": p_type["Lexema"], "id": p_id["Lexema"]})
            self.match("RPAREN")
            self.match("COLON")
            
            body = []
            while self.current_token() and not (self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["procedure", "function", "switch", "case", "default"]):
                stmt = self.parse_statement()
                if stmt: body.append(stmt)
            return {"type": "FunctionDeclaration", "name": id_tok["Lexema"], "parameters": params, "body": body}

        # 3. Declaração de Procedure
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "procedure":
            self.match("KEYWORD", "procedure")
            id_tok = self.match("ID")
            self.match("LPAREN")
            self.match("RPAREN")
            self.match("COLON")
            
            body = []
            while self.current_token() and not (self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["procedure", "function", "switch", "case", "default"]):
                stmt = self.parse_statement()
                if stmt: body.append(stmt)
            return {"type": "ProcedureDeclaration", "name": id_tok["Lexema"], "body": body}

        # 4. Condicional If / Else
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "if":
            self.match("KEYWORD", "if")
            self.match("LPAREN")
            condition = self.parse_expression()
            self.match("RPAREN")
            self.match("COLON")
            
            body = []
            while self.current_token() and not (self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["else", "procedure", "function", "switch", "case", "default"]):
                stmt = self.parse_statement()
                if stmt: body.append(stmt)
                
            else_body = []
            if self.current_token() and self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] == "else":
                self.match("KEYWORD", "else")
                self.match("COLON")
                while self.current_token() and not (self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["procedure", "function", "switch", "case", "default"]):
                    stmt = self.parse_statement()
                    if stmt: else_body.append(stmt)
            return {"type": "IfStatement", "condition": condition, "thenBody": body, "elseBody": else_body if else_body else None}

        # 5. Laço While
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "while":
            self.match("KEYWORD", "while")
            self.match("LPAREN")
            condition = self.parse_expression()
            self.match("RPAREN")
            self.match("COLON")
            
            body = []
            while self.current_token() and not (self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["procedure", "function", "switch", "case", "default"]):
                stmt = self.parse_statement()
                if stmt: body.append(stmt)
            return {"type": "WhileStatement", "condition": condition, "body": body}

        # 6. Múltipla Escolha (Switch/Case)
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "switch":
            self.match("KEYWORD", "switch")
            self.match("LPAREN")
            expr = self.parse_expression()
            self.match("RPAREN")
            self.match("COLON")
            
            cases = []
            while self.current_token() and self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["case", "default"]:
                case_tok = self.match("KEYWORD")
                case_val = None
                if case_tok["Lexema"] == "case":
                    case_val = self.match("NUMBER")["Lexema"]
                self.match("COLON")
                
                case_body = []
                while self.current_token() and not (self.current_token()["Token"] == "KEYWORD" and self.current_token()["Lexema"] in ["case", "default", "procedure", "function", "switch"]):
                    stmt = self.parse_statement()
                    if stmt: case_body.append(stmt)
                cases.append({"type": "SwitchCase" if case_val else "SwitchDefault", "value": case_val, "body": case_body})
            return {"type": "SwitchStatement", "discriminant": expr, "cases": cases}

        # 7. Comandos de Controle (return, break)
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "return":
            self.match("KEYWORD", "return")
            expr = self.parse_expression()
            self.match("PONTO_V")
            return {"type": "ReturnStatement", "argument": expr}
        
        elif tok["Token"] == "KEYWORD" and tok["Lexema"] == "break":
            self.match("KEYWORD", "break")
            self.match("PONTO_V")
            return {"type": "BreakStatement"}

        # 8. Atribuição Simples e Chamada de Função (ex: x = 10; ou move();)
        elif tok["Token"] == "ID":
            id_tok = self.match("ID")
            if self.current_token() and self.current_token()["Token"] == "ASSIGN":
                self.match("ASSIGN")
                expr = self.parse_expression()
                self.match("PONTO_V")
                return {"type": "AssignmentStatement", "id": id_tok["Lexema"], "value": expr}
            elif self.current_token() and self.current_token()["Token"] == "LPAREN":
                self.match("LPAREN")
                self.match("RPAREN")
                self.match("PONTO_V")
                return {"type": "CallStatement", "name": id_tok["Lexema"]}
        
        # Avança para não criar loop infinito em símbolos não mapeados
        self.pos += 1
        return None

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token()["Token"] in ["OP_ARIT", "OP_COMP", "LOGIC"]:
            op = self.current_token()
            self.pos += 1
            right = self.parse_term()
            left = {"type": "BinaryExpression", "operator": op["Lexema"], "left": left, "right": right}
        return left

    def parse_term(self):
        tok = self.current_token()
        if not tok: return None
        if tok["Token"] == "NUMBER":
            self.match("NUMBER")
            return {"type": "Literal", "value": tok["Lexema"]}
        elif tok["Token"] == "STRING":
            self.match("STRING")
            return {"type": "Literal", "value": tok["Lexema"]}
        elif tok["Token"] == "ID":
            id_tok = self.match("ID")
            return {"type": "Identifier", "name": id_tok["Lexema"]}
        elif tok["Token"] == "LPAREN":
            self.match("LPAREN")
            expr = self.parse_expression()
            self.match("RPAREN")
            return expr
        return None

    # Função para salvar a AST no arquivo JSON final do TDE
    def export_json(self, ast, filename="ast.json"):
        if ast:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(ast, f, indent=4, ensure_ascii=False)
            print(f"Sucesso! Árvore Sintática Abstrata exportada para '{filename}'.")