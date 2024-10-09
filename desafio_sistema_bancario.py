from datetime import datetime, date
from abc import ABC, abstractmethod, abstractproperty

# Interface Transacao

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# Classe Deposito

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

# Classe Saque
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

# Classe Historico

class Historico:
    def __init__(self):
        self._transacoes = list()

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            })


# Classe Conta

class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
            if valor > self._saldo:
                print(f'Operação Falhou! Não é possível efutuar o saque por falta de saldo.')
                return False
            else:
                self._saldo -= valor
                print(f'Saque de R$ {valor:.2f} efetuado com sucesso!')
                return True

    def depositar(self, valor):
        if valor < 0:
            print('Operação Falhou! Depósito tem que ser um valor positivo!')
            return False
        else:
            self._saldo += valor
            print(f'Depósito de R$ {valor:.2f} efetuado com sucesso!')
            return True

# Classe ContaCorrente
    
class ContaCorrente (Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3, limite_transacoes = 10):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._limite_transacoes = limite_transacoes

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self._historico._transacoes if transacao['tipo'] == Saque.__name__])
        numero_transacoes = len(self._historico._transacoes)

        if numero_saques == self._limite_saques:
            print('Operação Falhou! Não é possível sacar mais dinheiro hoje, tente novamente amanhã!')
        
        elif numero_transacoes > self._limite_transacoes:
            print('Operação Falhou! Você excedeu o número de transações permitidas no dia!')

        else:
            if valor > self._limite:
                print(f'Operação Falhou! O saque tem que ser de no máximo R$ {self._limite:.2f}!')
            
            else:
                return super().sacar(valor)
            
        return False
    
    def depositar(self, valor):
        numero_transacoes = len(self._historico._transacoes)

        if numero_transacoes > self._limite_transacoes:
            print('Operação Falhou! Você excedeu o número de transações permitidas no dia!')
            return False
        else:
            return super().depositar(valor)
        
    def __str__(self):
        return f'''
                Agência: \t {self.agencia}
                C/C: \t\t {self.numero}
                Titular: \t {self.cliente.nome}
                '''

# Classe Cliente
        
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = list()

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


# Classe Pessoas Fisica

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    def __str__(self):
        return f'''
                Nome do Titular: \t {self._nome}
                CPF: \t\t {self._cpf}
                Data Nascimento: \t {self._data_nascimento}
                Endereço: \t {self._endereco}
                '''

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

def cadastrar_usuario(lista_usuarios, nome, data_nascimento, cpf, *endereco):
    # Futuramente: Implementar uma função de verificação do CPF se o formato está correto
    resultado_cadastrado, cliente = verifica_usuario_cadastrado(cpf)
    if resultado_cadastrado:
        print('Operação Falhou! Já existe um usuário com esse CPF cadastrado.')
    else:
        # Formatando a Data de Nascimento
        data_nascimento = data_nascimento.strip()
        data_nascimento = list(data_nascimento.split(' '))
        data_nascimento = date(int(data_nascimento[2]), int(data_nascimento[1]), int(data_nascimento[0]))

        endereco_str = ' - '.join(endereco)

        lista_usuarios.append(PessoaFisica(endereco_str, cpf, nome, data_nascimento))

        print('Cadastro de Usuário Realizado com Sucesso!')
    
def cadastrar_conta(*, cpf, contas):
    resultado_cadastrado, cliente = verifica_usuario_cadastrado(cpf)
    if resultado_cadastrado:
        conta = ContaCorrente(len(lista_contas), cliente)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        
        print('Conta Cadastrada com Sucesso!')

def verifica_usuario_cadastrado(cpf):
    for usuario in lista_usuarios:
        if usuario.cpf == cpf:
            return True, usuario
    
    print(f'Operação Falhou! Não há nenhum usuário cadastrado com o cpf: {cpf}.')
    return False, None

def encontra_conta(cliente):
    for conta in lista_contas:
        if conta.cliente == cliente:
            return conta
    
    print(f'Operação Falhou! Não há nenhuma conta cadastrada para o cliente com o cpf: {cpf}.')    
    return None

def listar_usuarios(usuarios):
    if len(usuarios) > 0:
        for usuario in usuarios:
            print(usuario)
    else:
        print('Operação Falhou! Não há usuários cadastrados.')

def listar_contas(contas):
    if len(contas) > 0:
        for conta in contas:
            print(conta)
    else:
        print('Operação Falhou! Não há contas cadastradas.')

def realiza_operacao(cpf, valor, tipo_operacao, /):
    resultado_cadastrado, cliente = verifica_usuario_cadastrado(cpf)
    if resultado_cadastrado:
        conta = encontra_conta(cliente)
        if conta != None:
            if tipo_operacao == 'Deposito':
                conta.cliente.realizar_transacao(conta, Deposito(valor))
            else:
                conta.cliente.realizar_transacao(conta, Saque(valor))

def extrato(cpf):
    resultado_cadastrado, cliente = verifica_usuario_cadastrado(cpf)
    if resultado_cadastrado:
        conta = encontra_conta(cliente)
        if conta != None:
            print(conta.historico.transacoes)

lista_usuarios = []
lista_contas = []

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

        cadastrar_usuario(lista_usuarios, nome, data_nascimento, cpf, logradouro, bairro, cidade_estado) 

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
        cpf = input('Entre com o valor do CPF: ')
        valor = float(input('Entre com o valor do depósito: '))
            
        realiza_operacao(cpf, valor, 'Deposito')

    elif opcao == 's':
        print('Saque')

        cpf = input('Entre com o valor do CPF: ')
        valor = float(input('Entre com o valor do Saque: '))

        realiza_operacao(cpf, valor, 'Saque')

    elif opcao == 'e':
        print('Extrato')
        cpf = input('Entre com o valor do CPF: ')
        extrato(cpf)

    elif opcao == 'q':
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
