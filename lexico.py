"""

Instituto Federal de Minas Gerais - Campus Formiga

Jonathan Arantes <tlc.jooker@gmail.com>
Rúbia Marques <rubiamarquesoliveira@gmail.com>

"""

from os import path

class TipoToken:
    # Tokens
    ID = (1, 'ID')
    CTE = (2, 'NUM')
    CADEIA = (3, 'CADEIA')
    ATRIB = (4, ':=')
    OPREL = (5, 'OPREL')
    OPAD = (6, 'OPAD')
    OPMUL = (7, 'OPMUL')
    PVIRG = (8, ';')
    DPONTOS = (9, ':')
    VIRG = (10, ',')
    ABREPAR = (11, '(')
    FECHAPAR = (12, ')')
    ABRECH = (13, '{')
    FECHACH = (14, '}')
    # Palavras reservadas
    PROGRAMA = (15, 'PROGRAMA')
    VARIAVEIS = (16, 'VARIAVEIS')
    INTEIRO = (17, 'INTEIRO')
    REAL = (18, 'REAL')
    LOGICO = (19, 'LOGICO')
    CARACTER = (20, 'CARACTER')
    SE = (21, 'SE')
    SENAO = (22, 'SENAO')
    ENQUANTO = (23, 'ENQUANTO')
    LEIA = (24, 'LEIA')
    ESCREVA = (25, 'ESCREVA')
    FALSO = (26, 'FALSO')
    VERDADEIRO = (27, 'VERDADEIRO')
    # Error Token, nao esta presente na gramatica
    ERROR = (28, 'ERRO')
    FIMARQ = (29, 'EOF')
    OPNEG = (30, '!')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 
        'LEIA': TipoToken.LEIA,
        'ESCREVA': TipoToken.ESCREVA,
        'PROGRAMA': TipoToken.PROGRAMA,
        'VARIAVEIS': TipoToken.VARIAVEIS,
        'INTEIRO': TipoToken.INTEIRO,
        'REAL': TipoToken.REAL,
        'LOGICO': TipoToken.LOGICO,
        'CARACTER': TipoToken.CARACTER,
        'SE': TipoToken.SE,
        'SENAO': TipoToken.SENAO,
        'FALSO': TipoToken.FALSO,
        'VERDADEIRO': TipoToken.VERDADEIRO,
        'ENQUANTO': TipoToken.ENQUANTO
    }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    #Abre o arquivo se já não estiver aberto e se existir
    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres desalocados pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self) -> str:
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c.lower()
        else:
            c = ''
            try:
                c = self.arquivo.read(1)
            except UnicodeDecodeError:
                pass
            
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c: str):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        estado = 1
        car = None
        lexema = ''
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha += 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3  
                elif car in {':', '=', '<', '>', ',', ';', '+', '-', '*', '(', ')', '{', '}'}:
                    if car == ';':
                        self.linha += 1
                    estado = 4
                elif car == '/':
                    lexema = car
                    lexema += self.getChar()
                    if (lexema == '//' or lexema == '/*'):
                        estado = 5
                    else:
                        self.ungetChar(lexema[1:])
                        lexema = ''
                        estado = 4
                elif car == '"':
                    estado = 6
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = car
                while(car.isalnum()):
                    car = self.getChar()
                    lexema += car
                if (car is None) or (not car.isalnum()):
                    # terminou o nome
                    if not len(lexema) == 1:
                        self.ungetChar(car)
                        lexema = lexema[:-1].strip()
                    if lexema.upper() in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema.upper()], lexema, self.linha)
                    else:
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros e ponto flutuante
                lexema = car
                while(str(lexema)[-1] != ' ') and (car.isdigit() or car == '.'):
                    car = self.getChar()
                    lexema += car
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.CTE, lexema, self.linha)
                return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                if car == '=':
                    return Token(TipoToken.OPREL, car, self.linha)
                elif car == ':':
                    lexema = car
                    lexema += self.getChar()
                    if lexema == ':=':
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                    else:
                        self.ungetChar(lexema[-1])
                        return Token(TipoToken.DPONTOS, car, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, car, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, car, self.linha)
                elif car == '+':
                    return Token(TipoToken.OPAD, car, self.linha)
                elif car == '-':
                    return Token(TipoToken.OPAD, car, self.linha)
                elif car == '*':
                    return Token(TipoToken.OPMUL, car, self.linha)
                elif car == '/':
                    return Token(TipoToken.OPMUL, car, self.linha)
                elif car == '(':
                    return Token(TipoToken.ABREPAR, car, self.linha)
                elif car == ')':
                    return Token(TipoToken.FECHAPAR, car, self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, car, self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, car, self.linha)
                elif car == '<':
                    lexema = car
                    lexema += self.getChar()
                    if lexema == '<>':
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    elif lexema == '<=':
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(lexema[-1])
                        return Token(TipoToken.OPREL, car, self.linha)
                elif car == '>':
                    lexema = car
                    lexema += self.getChar()
                    if lexema == '>=':
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(lexema[-1])
                        return Token(TipoToken.OPREL, car, self.linha)
                return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 5:
                # consumindo comentario
                if lexema == '//':
                    while (not car is None) and (car != '\n'):
                        car = self.getChar()
                    estado = 1
                elif lexema == '/*':
                    while (estado != 1):
                        car = self.getChar()
                        if (car is None):
                            estado = 1
                            continue
                        if (car == '*'):
                            car = self.getChar()
                            if (car == '/'):
                                estado = 1
                                continue
            elif estado == 6:
                car = self.getChar()
                while (car != '"'):
                    lexema += car
                    car = self.getChar()
                return Token(TipoToken.CADEIA, lexema, self.linha)
