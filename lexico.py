"""

 Linguagem P
    Gramatica::

    G1 = {{PROG, DECLS, C-COMP, LIST-DECLS, DECL-TIPO, D, LIST-ID, E, TIPO, LISTACOMANDOS, G, COMANDOS, IF, WHILE, READ, ATRIB, WRITE, EXPR, H, LIST-W, L, ELEM-W, SIMPLES, P, R, TERMO, S, FAT}{programa, id, variaveis, inteiro, real, logico, caracter, abrepar, fechapar, se, abrech, fechach, senao, enquanto, leia, atrib, escreva, cadeia, cte, verdadeiro, falso, oprel, opad, opmul, opneg, pvirg, virg, dpontos}, P, PROG} 
    
    P={ PROG → programa id pvirg DECLS C-COMP
        DECLS → $ | variaveis  LIST-DECLS
        LIST-DECLS → DECL-TIPO D
        D → $ | LIST-DECLS 
        DECL-TIPO → LIST-ID dpontos TIPO pvirg 
        LIST-ID → id E
        E → $ | virg LIST-ID 
        TIPO → inteiro | real | logico | caracter
        C-COMP → abrech LISTA-COMANDOS fechach 
        LISTA-COMANDOS → COMANDOS G 
        G → $ | LISTA-COMANDOS 
        COMANDOS → IF | WHILE | READ | WRITE | ATRIB 
        IF → se abrepar EXPR fechapar C-COMP H 
        H → $ | senao C-COMP 
        WHILE → enquanto abrepar EXPR fechapar C-COMP 
        READ → leia abrepar LIST-ID fechapar pvirg 
        ATRIB → id atrib EXPR pvirg 
        WRITE → escreva abrepar LIST-W fechapar pvirg 
        LIST-W → ELEM-W L 
        L → $ | virg LIST-W 
        ELEM-W → EXPR | cadeia 
        EXPR → SIMPLES P 
        P → $ | oprel SIMPLES 
        SIMPLES → TERMO R 
        R → $ | opad SIMPLES 
        TERMO → FAT S 
        S → $ | opmul TERMO 
        FAT → id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT}


    Tokens::

    ID CTE CADEIA ATRIB OPREL OPAD OPMUL OPNEG PVIRG DPONTOS VIRG ABREPAR FECHAPAR ABRECH FECHACH

    Palavras reservadas::

    PROGRAMA, VARIAVEIS, INTEIRO, REAL, LOGICO, CARACTER, SE, SENAO, ENQUANTO, LEIA, ESCREVA, FALSO, VERDADEIRO

    Tipos basicos::

    INTEIRO, REAL, LOGICO, CARACTER

    Comentarios::

    iniciam com // ate o fim da linha

    /*
        
    */

"""

from os import path

class TipoToken:
    IDENT = (1, 'ident')
    ATRIB = (2, '=')
    READ = (3, 'read')
    PTOVIRG = (4, ';')
    PRINT = (5, 'print')
    ADD = (6, '+')
    MULT = (7, '*')
    OPENPAR = (8, '(')
    CLOSEPAR = (9, ')')
    NUM = (10, 'numero')
    ERROR = (11, 'erro')
    FIMARQ = (12, 'fim-de-arquivo')

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
    reservadas = { 'print': TipoToken.PRINT, 'read': TipoToken.READ }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
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

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car in {'=', ';', '+', '*', '(', ')'}:
                    estado = 4
                elif car == '#':
                    estado = 5
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        return Token(TipoToken.IDENT, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.NUM, lexema, self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '=':
                    return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PTOVIRG, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.ADD, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.MULT, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)
            elif estado == 5:
                # consumindo comentario
                while (not car is None) and (car != '\n'):
                    car = self.getChar()
                self.ungetChar(car)
                estado = 1


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo.toy'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
