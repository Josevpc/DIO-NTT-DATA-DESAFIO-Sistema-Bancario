from datetime import datetime as dt

menu = '''

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> '''

saldo = 0
LIMITE_SAQUE = 500
extrato = ''
numero_saques = 0

QUANTIDADE_LIMITE_SAQUES = 3
QUANTIDADE_LIMITE_TRANSACOES = 10

# Faço a verificação de quantas movimentações foram realizadas pelo len(operacoes) == QUANTIDADE_LIMITE_TRANSACOES
operacoes = []
operacoes_saldo_atual = []
operacoes_saldo_novo = []
operacoes_dia = []


def cadastrar_operacoes(*, operacao, saldo_atual, saldo_novo):
    operacoes.append(operacao)
    operacoes_saldo_atual.append(saldo_atual)
    operacoes_saldo_novo.append(saldo_novo)
    operacoes_dia.append(dt.now())


while True:

    opcao = input(menu)

    if opcao == 'd':
        print('Depósito')

        if len(operacoes) == QUANTIDADE_LIMITE_TRANSACOES:
            print('Operação Falhou! Você excedeu o número de transações permitidas no dia!')

        else:
            while True:
                valor = float(input('Entre com o valor do depósito: '))
                if valor < 0:
                    print('Operação Falhou! Depósito tem que ser um valor positivo!')
                else:
                    break

            saldo_novo = saldo + valor

            cadastrar_operacoes(operacao='Depósito',saldo_atual=saldo, saldo_novo=saldo_novo)

            saldo = saldo_novo

            print(f'Depósito de R$ {valor:.2f} efetuado com sucesso!')

    elif opcao == 's':
        print('Saque')

        if len(operacoes) == QUANTIDADE_LIMITE_TRANSACOES:
            print('Operação Falhou! Você excedeu o número de transações permitidas no dia!')

        if numero_saques == QUANTIDADE_LIMITE_SAQUES:

            print('Operação Falhou! Não é possível sacar mais dinheiro hoje, tente novamente amanhã!')

        else:
            while True:
                valor = float(input('Entre com o valor do Saque: '))

                if valor > LIMITE_SAQUE:
                    print(f'Operação Falhou! O saque tem que ser de no máximo R$ {LIMITE_SAQUE:.2f}!')

                else:
                    if valor > saldo:
                        print(
                            f'Operação Falhou! Não é possível efutuar o saque por falta de saldo.')
                    else:
                        break

            numero_saques += 1

            saldo_novo = saldo - valor

            cadastrar_operacoes(operacao='Saque', saldo_atual=saldo, saldo_novo=saldo_novo)

            saldo = saldo_novo

            print(f'Saque de R$ {valor:.2f} efetuado com sucesso!')

    elif opcao == 'e':
        print('Extrato')

        print('-' * 10)

        if len(operacoes) != 0:
            for index in range(0, len(operacoes)):
                print(f'Operação: {operacoes[index]}')
                print(f'Saldo Anterior: {operacoes_saldo_atual[index]:.2f}')
                print(f'Saldo Atual: {operacoes_saldo_novo[index]:.2f}')
                print(f'Data da Operação: {operacoes_dia[index].strftime('%d/%m/%Y %H:%M')}')
                print('-' * 10)
        else:
            print('Não foram realizadas movimentações')
    elif opcao == 'q':
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
