# Relatório de Trabalho - Compilador da Linguagem P

Jonathan Arantes Pinto - 0021625 <tlc.jooker@gmail.com>

## Sobre o Trabalho

Neste trabalho foram desenvolvidos os analisadores léxico e sintático da linguagem de programação P, seguindo de acordo com a gramática descrita na documentação do trabalho.

O analisador léxico realiza a leitura do arquivo de entrada com o código escrito na linguagem P, onde cada palavra/símbolo é classificada em um Token e entregue para o analisador sintático de forma iterativa, apenas uma palavra por vez é lida e entregue, este não realiza a leitura de todo o arquivo antes de classificar os tokens.

O analisador sintático realiza a interpretação dos tokens na ordem em que são lidos, de forma a concordar com a gramática descrita para a linguagem.

## Tabela de Símbolos

A tabela de símbolos é gerada pelo analisador sintático, em que este é preenchido a cada etapa em que ocorre a iteração com o analisador léxico, preenchendo uma ___lista___ que é exibida (apenas os identificadores dos tokens, uma vez que não foi descrito uma saída específica para a tabela de símbolos, foi decidido em apenas exibir os identificadores para fins de testes).

## Tratamento de erros

Erros durante a classificação dos tokens (erros léxicos) foram tratados considerando que tokens inválidos não são lidos nem entregues ao analisador sintático.

__OBS__: Erros sintáticos não foram tratados, portanto apenas o primeiro erro encontrado é exibido antes do encerramento da execução.

__OBS2__: Caracteres inválidos não são reconhecidos pelo leitor de arquivo do _Python3_, pois este utiliza por padrão o formato UTF-8, impedindo a leitura do arquivo, e este erro não foi corrigido a tempo da entrega.