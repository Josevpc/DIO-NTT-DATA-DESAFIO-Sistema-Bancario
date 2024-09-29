# Sistema Bancário Básico

Este repositório contém a minha solução para o desafio proposto no **Bootcamp NTT DATA - Engenharia de Dados** da [DIO](https://www.dio.me/). O desafio consistia na criação de um sistema bancário básico utilizando Python, com funções de **depósito**, **saque** e **extrato** para gerenciar uma única conta.

## Funcionalidades

O sistema desenvolvido possui as seguintes funcionalidades:

- **Depósito**: Adiciona um valor à conta bancária.
- **Saque**: Permite a retirada de um valor da conta, com as seguintes regras:
  - Limite de **3 saques diários**.
  - Cada saque pode ser de, no máximo, **R$500**.
  - Não é permitido realizar saques se o valor for maior que o saldo disponível (saques negativos).

- **Extrato**: Exibe o histórico de transações realizadas (depósitos e saques), bem como o saldo atual da conta.
- **Cadastrar Usuário**: Recebe informações do usuário, como nome, data de nascimento, CPF e endereço. Caso o CPF não esteja cadastrado, cria um novo usuário.
- **Criar Contar**: Recebe o CPF do usuário e, caso já exista um usuário cadastrado com esse CPF, cria uma nova conta.

## Tecnologias Utilizadas

- **Python 3**: Linguagem de programação utilizada para desenvolver o sistema.
