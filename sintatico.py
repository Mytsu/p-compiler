"""

 Linguagem P
    Gramatica::

    G1 = {{PROG, DECLS, C-COMP, LIST-DECLS, DECL-TIPO, D, LIST-ID, E, TIPO, LISTACOMANDOS, G, COMANDOS, IF, WHILE, READ, ATRIB, WRITE, EXPR, H, LIST-W, L, ELEM-W, SIMPLES, P, R, TERMO, S, FAT}{programa, id, variaveis, inteiro, real, logico, caracter, abrepar, fechapar, se, abrech, fechach, senao, enquanto, leia, atrib, escreva, cadeia, cte, verdadeiro, falso, oprel, opad, opmul, opneg, pvirg, virg, dpontos}, P, PROG} 
    
    P={ 
        A → PROG $
        PROG → programa id pvirg DECLS C-COMP
        DECLS → λ | variaveis  LIST-DECLS
        LIST-DECLS → DECL-TIPO D
        D → λ | LIST-DECLS 
        DECL-TIPO → LIST-ID dpontos TIPO pvirg 
        LIST-ID → id E
        E → λ | virg LIST-ID 
        TIPO → inteiro | real | logico | caracter
        C-COMP → abrech LISTA-COMANDOS fechach 
        LISTA-COMANDOS → COMANDOS G 
        G → λ | LISTA-COMANDOS 
        COMANDOS → IF | WHILE | READ | WRITE | ATRIB 
        IF → se abrepar EXPR fechapar C-COMP H 
        H → λ | senao C-COMP 
        WHILE → enquanto abrepar EXPR fechapar C-COMP 
        READ → leia abrepar LIST-ID fechapar pvirg 
        ATRIB → id atrib EXPR pvirg 
        WRITE → escreva abrepar LIST-W fechapar pvirg 
        LIST-W → ELEM-W L 
        L → λ | virg LIST-W 
        ELEM-W → EXPR | cadeia 
        EXPR → SIMPLES P 
        P → λ | oprel SIMPLES 
        SIMPLES → TERMO R 
        R → λ | opad SIMPLES 
        TERMO → FAT S 
        S → λ | opmul TERMO 
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

from lexico import TipoToken as tt, Token, Lexico
from sys import argv

class Sintatico:

    def __init__(self, gerar_tokens: bool):
        self.lex = None
        self.tokenAtual = None
        self.gerar_tokens = gerar_tokens
        self.tokens = []

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            if self.gerar_tokens:
                self.tokens.append(self.tokenAtual)

            self.A()

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, _) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual( token ):
            self.tokenAtual = self.lex.getToken()
            if self.gerar_tokens:
                self.tokens.append(self.tokenAtual)
        else:
            (_, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def A(self):
        self.PROG()
        self.consome( tt.FIMARQ )

    def PROG(self):
        self.consome( tt.PROGRAMA )
        self.consome( tt.ID )
        self.consome( tt.PVIRG )
        self.DECLS()
        self.C_COMP()
    
    def DECLS(self):
        if not self.atualIgual( tt.VARIAVEIS ):
            pass
        else:
            self.consome( tt.VARIAVEIS )
            self.LIST_DECLS()
    
    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()
    
    def D(self):
        if not self.atualIgual( tt.ID ):
            pass
        else:
            self.LIST_DECLS()
    
    def DECL_TIPO(self):
        self.LIST_ID()
        self.consome( tt.DPONTOS )
        self.TIPO()
        self.consome( tt.PVIRG )

    def LIST_ID(self):
        self.consome( tt.ID )
        self.E()

    def E(self):
        if not self.atualIgual( tt.VIRG ):
            pass
        else:
            self.consome( tt.VIRG )
            self.LIST_ID()

    def TIPO(self):
        if self.atualIgual( tt.INTEIRO ):
            self.consome( tt.INTEIRO )
        elif self.atualIgual( tt.REAL ):
            self.consome( tt.REAL )
        elif self.atualIgual( tt.LOGICO ):
            self.consome( tt.LOGICO )
        elif self.atualIgual( tt.CARACTER ):
            self.consome( tt.CARACTER )

    def C_COMP(self):
        self.consome( tt.ABRECH )
        self.LISTA_COMANDOS()
        self.consome( tt.FECHACH )

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    def G(self):
        if not (self.atualIgual( tt.SE ) or self.atualIgual( tt.ENQUANTO ) or self.atualIgual( tt.LEIA ) or self.atualIgual( tt.ESCREVA ) or self.atualIgual( tt.ID )): 
            pass
        else:
            self.LISTA_COMANDOS()

    def COMANDOS(self):
        if self.atualIgual( tt.SE ):
            self.IF()
        elif self.atualIgual( tt.ENQUANTO ):
            self.WHILE()
        elif self.atualIgual( tt.LEIA ):
            self.READ()
        elif self.atualIgual( tt.ESCREVA ):
            self.WRITE()
        elif self.atualIgual( tt.ID ):
            self.ATRIB()

    def IF(self):
        self.consome( tt.SE )
        self.consome( tt.ABREPAR )
        self.EXPR()
        self.consome( tt.FECHAPAR )
        self.C_COMP()
        self.H()

    def H(self):
        if not (self.atualIgual( tt.SENAO )):
            pass
        else:
            self.consome( tt.SENAO )
            self.C_COMP()

    def WHILE(self):
        self.consome( tt.ENQUANTO )
        self.consome( tt.ABREPAR )
        self.EXPR()
        self.consome( tt.FECHAPAR )
        self.C_COMP()

    def READ(self):
        self.consome( tt.LEIA )
        self.consome( tt.ABREPAR )
        self.LIST_ID()
        self.consome( tt.FECHAPAR )
        self.consome( tt.PVIRG )

    def ATRIB(self):
        self.consome( tt.ID )
        self.consome( tt.ATRIB )
        self.EXPR()
        self.consome( tt.PVIRG )

    def WRITE(self):
        self.consome( tt.ESCREVA )
        self.consome( tt.ABREPAR )
        self.LIST_W()
        self.consome( tt.FECHAPAR )
        self.consome( tt.PVIRG )

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if not self.atualIgual( tt.VIRG ):
            pass
        else:
            self.consome( tt.VIRG )
            self.LIST_W()
    
    def ELEM_W(self):
        if not self.atualIgual( tt.CADEIA ):
            self.EXPR()
        else:
            self.consome( tt.CADEIA )

    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        if not self.atualIgual( tt.OPREL ):
            pass
        else:
            self.consome( tt.OPREL )
            self.SIMPLES()

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        if not self.atualIgual( tt.OPAD ):
            pass
        else:
            self.consome( tt.OPAD )
            self.SIMPLES()

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        if not self.atualIgual( tt.OPMUL ):
            pass
        else:
            self.consome( tt.OPMUL )
            self.TERMO()

    def FAT(self):
        if self.atualIgual( tt.ID ):
            self.consome( tt.ID )
        elif self.atualIgual( tt.CTE ):
            self.consome( tt.CTE )
        elif self.atualIgual( tt.ABREPAR ):
            self.consome( tt.ABREPAR )
            self.EXPR()
            self.consome( tt.FECHAPAR )
        elif self.atualIgual( tt.VERDADEIRO ):
            self.consome( tt.VERDADEIRO )
        elif self.atualIgual( tt.FALSO ):
            self.consome( tt.FALSO )
        elif self.atualIgual( tt.OPNEG ):
            self.consome( tt.OPNEG )
            self.FAT()

if __name__== "__main__":

    #nome = input("Entre com o nome do arquivo: ")
    nome = argv[1]
    parser = Sintatico(True)
    try:
        parser.interprete(nome)
    finally:
        tokens = []
        for token in parser.tokens:
            tokens.append(token.msg)
        print(tokens)
    
