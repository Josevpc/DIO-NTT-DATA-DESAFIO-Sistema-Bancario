from datetime import datetime, date

saldo = 0
LIMITE_SAQUE = 500
extrato = ''
numero_saques = 0

QUANTIDADE_LIMITE_SAQUES = 3
QUANTIDADE_LIMITE_TRANSACOES = 10

# Faço a verificação de quantas movimentações foram realizadas pelo len(operacoes) == QUANTIDADE_LIMITE_TRANSACOES

'''
# Templates do Sistema de Manipulação de Contas em Operações Usando Dicionários para o Futuro
modelo_usuario = ['nome', 'data de nascimento', 'endereço']
modelo_endereco = ['logradouro', 'bairro', 'cidade', 'sigla estado']
modelo_conta = ['agencia', 'numero_conta', 'cpf_usuario', 'operacoes']
modelo_operacoes = ['tipo', 'saldo_anterior', 'saldo_atual', 'dia_hora']
'''

lista_usuarios = []
lista_contas = []

operacoes = []
operacoes_saldo_atual = []
operacoes_saldo_novo = []
operacoes_dia = []

def menu():
    menu = '''
    [u]  Cadastrar Usuário
    [c]  Criar Conta Corrente
    [lu] Listar Usuários
    [lc] Listar Contas
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [q]  Sair

    => '''
    return input(menu)

def cadastrar_operacoes(*, operacao, saldo_atual, saldo_novo):
    operacoes.append(operacao)
    operacoes_saldo_atual.append(saldo_atual)
    operacoes_saldo_novo.append(saldo_novo)
    operacoes_dia.append(datetime.now())

def cadastrar_usuario(nome, data_nascimento, cpf, *endereco):
    usuario = []
    # Futuramente: Implementar uma função de verificação do CPF se o formato está correto
    if verifica_usuario_cadastrado(cpf):
        print('Operação Falhou! Já existe um usuário com esse CPF cadastrado.')
        return None
    else:
        # Formatando a Data de Nascimento
        data_nascimento = data_nascimento.strip()
        data_nascimento = list(data_nascimento.split(' '))
        data_nascimento = date(int(data_nascimento[2]), int(data_nascimento[1]), int(data_nascimento[0]))

        endereco_str = ' - '.join(endereco)

        usuario = [{'nome':nome, 'data_nascimento':data_nascimento, 'cpf':cpf, 'endereco':endereco_str}]

        print('Cadastro de Usuário Realizado com Sucesso!')

        return usuario
    
def cadastrar_conta(*, cpf, contas):
    agencia = '0001'
    if verifica_usuario_cadastrado(cpf):
        conta_cadastrada = verifica_usuario_conta_cadastrado(cpf)
        if conta_cadastrada != None:
            # Metódo len(lista_contas) + 1 não fuciona pois um cpf agora pode ter mais contas viculadas e essas contas não estão listadas na lista de contas
            conta_cadastrada[cpf].append({'numero':len(lista_contas) + 1, 'agencia':agencia})
        else:
            conta = {cpf:[{'numero':len(lista_contas) + 1, 'agencia':agencia}]}
            contas.append(conta)
        
        print('Conta Cadastrada com Sucesso!')

    else:
        print('Operação Falhou! Não existe um usuário com esse CPF cadastrado.')

def verifica_usuario_cadastrado(cpf):
    for usuario in lista_usuarios:
        if usuario[0]['cpf'] == cpf:
            return True
    return False

def verifica_usuario_conta_cadastrado(cpf):
    for conta in lista_contas:
        if cpf in conta:
            return conta
    return None

def listar_usuarios(lista_usuarios):
    if len(lista_usuarios) > 0:
        for usuario in lista_usuarios:
            print(usuario)
    else:
        print('Operação Falhou! Não há usuários cadastrados.')

def listar_contas(contas):
    if len(contas) > 0:
        for conta in contas:
            print(conta)
    else:
        print('Operação Falhou! Não há contas cadastradas.')


def deposito(saldo, valor, /):
        if valor < 0:
            print('Operação Falhou! Depósito tem que ser um valor positivo!')
            return None
        else:
            return saldo + valor

def saque(*, saldo, valor, limite, numero_saques, limite_saques):
    if numero_saques == limite_saques:
        print('Operação Falhou! Não é possível sacar mais dinheiro hoje, tente novamente amanhã!')
        return None, numero_saques

    else:
        while True:

            if valor > limite:
                print(f'Operação Falhou! O saque tem que ser de no máximo R$ {LIMITE_SAQUE:.2f}!')
                return None, numero_saques

            if valor > saldo:
                print(f'Operação Falhou! Não é possível efutuar o saque por falta de saldo.')
                return None,  numero_saques
            
            else:
                return saldo - valor, numero_saques + 1
            
def extrato():
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


while True:

    opcao = menu()

    if opcao == 'u':
        print('Cadastro de Usuário')
        nome = input('Qual o seu nome ?')
        data_nascimento = input('Qual é a sua data de nascimento? (Ex: dd mm AAAA)')
        cpf = input('Qual o seu cpf ?')
        print('Agora serão realizadas perguntas sobre seu endereço')
        logradouro = input('Qual o Logradouro e número de sua residência ? (Ex: Casa, 202)')
        bairro = input('Qual o bairro de sua residência ?')
        cidade_estado = input('Qual a cidade e a sigla do estado em que se encontra sua residência? Ex: (Londrina/PR)')

        usuario = cadastrar_usuario(nome, data_nascimento, cpf, logradouro, bairro, cidade_estado) 
        
        if usuario !=  None:
            lista_usuarios.append(usuario)

    elif opcao == 'c':
        print('Criar Conta Corrente')
        cpf_usuario = input('Digite seu CPF (é necessário ter um cadastro de usuário prévio): ')

        cadastrar_conta(cpf=cpf_usuario, contas=lista_contas)

    elif opcao == 'lu':
        print('Listar Usuários')
        listar_usuarios(lista_usuarios)
    
    elif opcao == 'lc':
        print('Listar Contas')
        listar_contas(lista_contas)

    elif opcao == 'd':
        print('Depósito')

        if len(operacoes) == QUANTIDADE_LIMITE_TRANSACOES:
            print('Operação Falhou! Você excedeu o número de transações permitidas no dia!')

        else:
            while True:
                valor = float(input('Entre com o valor do depósito: '))
                
                saldo_novo = deposito(saldo, valor)

                if saldo_novo != None:
                    break

            cadastrar_operacoes(operacao='Depósito',saldo_atual=saldo, saldo_novo=saldo_novo)

            saldo = saldo_novo

            print(f'Depósito de R$ {valor:.2f} efetuado com sucesso!')

    elif opcao == 's':
        print('Saque')

        if len(operacoes) == QUANTIDADE_LIMITE_TRANSACOES:
            print('Operação Falhou! Você excedeu o número de transações permitidas no dia!')
        
        else:

            valor = float(input('Entre com o valor do Saque: '))

            saldo_novo, numero_saques = saque(saldo=saldo, valor=valor, limite=LIMITE_SAQUE, numero_saques=numero_saques, limite_saques=QUANTIDADE_LIMITE_SAQUES)

            if saldo_novo != None:
                cadastrar_operacoes(operacao='Saque', saldo_atual=saldo, saldo_novo=saldo_novo)

                saldo = saldo_novo

                print(f'Saque de R$ {valor:.2f} efetuado com sucesso!')

    elif opcao == 'e':
        print('Extrato')
        extrato()

    elif opcao == 'q':
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
