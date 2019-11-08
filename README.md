# Trabalho de Compiladores I
#### Jonathan Arantes <tlc.jooker@gmail.com>

#### Rúbia Marques <rubiamarquesoliveira@gmail.com>

Este projeto contem analisadores léxico e sintático bem como a geração da tabela de símbolos para a linguagem de programação P, gerada pela gramática apresentada abaixo:

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

    multilinha inicia com /* e terminam com */

## Como utilizar

Utilize o ___Python3___ para executar o arquivo _main.py_, passando o nome do arquivo como argumento, ex:

```python3 main.py ./exemplos/exemplo1.txt```

### Tabela de Símbolos

Para visualizar a tabela de símbolos utilize o argumento _-t_ seguido do nome do arquivo de saída, ex:

```python3 main.py ./exemplos/exemplo1.txt -t saida.txt```