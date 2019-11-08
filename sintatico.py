"""

Instituto Federal de Minas Gerais - Campus Formiga

Jonathan Arantes <tlc.jooker@gmail.com>
Rúbia Marques <rubiamarquesoliveira@gmail.com>

"""

from lexico import TipoToken as tt, Token, Lexico

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
