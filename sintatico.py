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

from lexico import TipoToken as tt, Token, Lexico

class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.F()
            self.consome( tt.FIMARQ )

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual( token ):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def F(self):
        self.C()
        self.Rf()

    def Rf(self):
        if self.atualIgual( tt.FIMARQ ):
            pass
        else:
            self.C()
            self.Rf()

    def C(self):
        if self.atualIgual( tt.READ ):
            self.R()
        elif self.atualIgual( tt.PRINT ):
            self.P()
        else:
            self.A()

    def A(self):
        self.consome( tt.IDENT )
        self.consome( tt.ATRIB )
        self.E()
        self.consome( tt.PTOVIRG )

    def R(self):
        self.consome( tt.READ )
        self.consome( tt.OPENPAR )
        self.consome( tt.IDENT )
        self.consome( tt.CLOSEPAR )
        self.consome( tt.PTOVIRG )

    def P(self):
        self.consome( tt.PRINT )
        self.consome( tt.OPENPAR )
        self.consome( tt.IDENT )
        self.consome( tt.CLOSEPAR )
        self.consome( tt.PTOVIRG )

    def E(self):
        self.M()
        self.Rs()

    def Rs(self):
        if self.atualIgual( tt.ADD ):
            self.consome( tt.ADD )
            self.M()
            self.Rs()
        else:
            pass

    def M(self):
        self.Op()
        self.Rm()

    def Rm(self):
        if self.atualIgual( tt.MULT ):
            self.consome( tt.MULT )
            self.Op()
            self.Rm()
        else:
            pass

    def Op(self):
        if self.atualIgual( tt.OPENPAR ):
            self.consome( tt.OPENPAR )
            self.E()
            self.consome( tt.CLOSEPAR )
        else:
            self.consome( tt.NUM )

if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo11.txt'
   parser = Sintatico()
   parser.interprete(nome)
