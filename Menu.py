from datetime import *

lista_clientes = []


#Funções
#Pega as informações dos clientes nos arquivo e guarda na lista respectiva
with open('clientes.txt', 'r') as arq:
    for clientes in arq.readlines():
        lista_clientes.append(eval(clientes))

#Mensagem de retorno ao menu
def retMenu(msg):
    #Pega a Exceção que vier de alguma função para cancelar ela e printa a mensagem de cancelamento
    print()
    print(msg)
    print()
    print()


#Salva uma nova operação no extrato
def newOp(cnpj, op, valor, newSaldo, taxa = 0):
    #Pega o horário atual e as informações da operação realizada formata em string e guarda em uma lista no dicionário do cliente
    tempoAtual = datetime.now()
    horario = tempoAtual.strftime("Data: %d/%m/%Y, %H:%M:%S")
    horario = f'{"%s " % horario: <{30}}'
    
    valorOp = f'{"%s %.2f " % (op, valor): <{15}}'
    tarifa = f'{"Tarifa: R$%.2f " % taxa: <{20}}'
    newSaldo = "Saldo: R$%.2f" % newSaldo
    
    
    op = horario + tarifa + valorOp + newSaldo
    
    for cliente in lista_clientes:
        if cnpj == cliente['cnpj']:
            cliente['extrato'].append(op)
            save()
            break

#Verifica se a entrada de valor possui no máximo 2 casas decimais e propaga a exceção se o número for negativo ou ter mais de duas casas decimais
def verifValue(n):
    if n < 0:
        raise ValueError
    x = str(n).split('.')

    if len(x[1]) > 2:
        raise ValueError

#Verifica os inputs das funções, se for igual a 0, ela é encerrada e retorna ao menu
def ret(x=1):
    if x == 0 or x == '0':
        raise Exception("Retorno ao menu de Opções.")
    else:
        return
    

#Salva as modificações nos Arquivos toda vez que uma função é executada
def save():
    with open('clientes.txt', 'w') as arq:
        for clientes in lista_clientes:
            arq.write('%s\n' % str(clientes))

        
#1. Novo Cliente
def newClient():
    global lista_clientes
    verifi = True
    
    print()
    print("Digite seus dados:")
    print()
    # Faz a verificação do cnpj para saber se é um número inteiro maior que 0
    while (True):
        try:
            cnpj = int(input("CNPJ: "))
            if cnpj < 0:
                raise ValueError
            else:
                break
        except ValueError:
            print("CNPJ Inválido")
    ret(cnpj)
    
    # Abre a lista de clientes e verifica se o cnpj já foi cadastrado
    for clientes in lista_clientes:
        if cnpj == clientes['cnpj']:
            verifi = False
            print()
            print("CNPJ já cadastrado.")
            print()
            break
        else:
            verifi = True
    
    # Se não existir clientes com esse cnpj já cadastrado, continua a função
    if verifi:
        razaoSocial = input("Razão Social: ")
        ret(razaoSocial)
        # Permite que apenas as opções 1 e 2 sejam aceitas
        while(True):
            tipoConta = input("Tipo de conta (1. Comum/2. Plus): ")
            ret(tipoConta)
            if tipoConta == '1':
                tipoConta = 'Comum'
                break
            elif tipoConta == '2':
                tipoConta = 'Plus'
                break
            else:
                print()
                print("Opção inválida")
                print()
                
        # Verifica o saldo e só permite valor positivo com no maximo duas casas decimais
        while (True):
            try:
                saldo = float(input("Digite o valor do depósito inicial: "))
                verifValue(saldo)
                break
            except ValueError:
                print("Valor Inválido")
            
        ret(saldo)
        
        senha = input("Digite sua nova senha: ")
        ret(senha)
        
        # Pega todos os dados e salva em um dicionário que é guardado numa lista temporária
        dados_cliente = {}
        dados_cliente["cnpj"] = cnpj
        dados_cliente["razaoSocial"] = razaoSocial
        dados_cliente["tipoConta"] = tipoConta
        dados_cliente["saldo"] = saldo
        dados_cliente["senha"] = senha

        # Cria as primeiras linhas do extrato e salva
        tempoAtual = datetime.now()
        horario = tempoAtual.strftime("Data: %d/%m/%Y, %H:%M:%S")
        horario = f'{"%s " % horario: <{64}}'

        dadosExtr = [f'Razao Social: {razaoSocial}', f'CNPJ: {cnpj}', f'Conta: {tipoConta}', f'{"%s Saldo: R$%.2f" % (horario, saldo)}']
        
        dados_cliente["extrato"] = dadosExtr

        lista_clientes.append(dados_cliente)

        # salva no arquivo as modificações
        save()
        
        print()
        print("Cliente cadastrado com sucesso!")
        print()
        
    
#2. Apaga cliente
def delClient():
    verif = False
    global lista_clientes
    print()
    print("Apagar Client:")
    print()
    while (True):
        try:
            cnpj = int(input("Digite o CNPJ: "))
            break
        except ValueError:
            print("CNPJ Inválido")
    
    ret(cnpj)

    # entra na lista de clienetes e verifica se a senha está correta
    for x in range(len(lista_clientes)):
        dicio = lista_clientes[x]
        if dicio['cnpj'] == cnpj:
            senha = input("Digite sua senha: ")
            ret(senha)
            verif = False
            if senha == dicio['senha']: # se a senha for correta apaga o cliente da lista e salva as modificações
                lista_clientes.pop(x)
                
                print()
                print("O cliente, de CNPJ: %d, foi apagado com Sucesso." % cnpj)
                print()
                
                break
            else:
                print()
                print("Senha Inválida")
                print()
                break
        else:
            verif = True
    
    if verif: #Se o cnpj não foi encontrado anteriormente isso é printado
        print()
        print("CNPJ não encontrado")
        print()

    save()


#3. Listar clientes
# Abre a lista de clientes e printa todos os clientes
def clientList():
    print()
    if len(lista_clientes) > 0:
        print("Esta é a lista de Clientes:")
        print()
        for x in lista_clientes:
            print("Razão Social: %s" % x['razaoSocial'])
            print("CNPJ: %d" % x['cnpj'])
            print("Saldo: R$%.2f" % x['saldo'])
            print("Tipo de Conta: %s" % x['tipoConta'])
            print()
    elif len(lista_clientes) == 0:
        print("Ainda não existem clientes cadastrados.")
        print()
    else:
        print("Erro")
        print()


#4. Saque
def saque():
    verif = False
    print()
    print("Digite seus dados para realizar o débito em conta:")
    print()

    while (True):
        try:
            cnpj = int(input("Digite o CNPJ: "))
            break
        except ValueError:
            print("CNPJ Inválido")
            
    ret(cnpj)
    
    # Abre a lista e verifica o cnpj e a senha
    for dicio in lista_clientes:
        if dicio['cnpj'] == cnpj:
            verif = False
            senha = input("Senha: ")
            ret(senha)
            verif = False
            if dicio['senha'] == senha:
                print()
                print("Saldo em conta: %.2f" % dicio['saldo'])
                while (True):
                    try:
                        valor = float(input("Valor do débito: "))
                        verifValue(valor)
                        break
                        
                    except ValueError:
                        print("Valor Inválido")
                ret(valor)
                # realiza o débito dependendo do tipo de conta
                if dicio['tipoConta'] == 'Comum':
                    taxa = round((valor * 0.05), 2)
                    if dicio['saldo'] - valor - taxa >= -1000:
                        dicio['saldo'] -= round((valor + taxa), 2)

                        print()
                        print("Saque do valor de: R$%.2f, Realizado" % valor)
                        print("O Valor da taxa de 5%% do seu Saque foi de: R$%.2f" % taxa)
                        print()
                        print("Seu novo saldo é de: R$%.2f" % dicio['saldo'])
                        print()
                        
                        newOp(cnpj, '-', valor, dicio['saldo'], taxa) # Salva a operação no extrato

                        break
                    else: # se a operação exceder o limite é mostrada esta mensagem
                        print()
                        print("Essa operação excede o valor minímo do seu tipo de conta")
                        print()
                        
                        break
                else:
                    taxa = round((valor * 0.03), 2)
                    if dicio['saldo'] - valor - taxa >= -5000:
                        dicio['saldo'] -= round((valor + taxa), 2)

                        print()
                        print("Saque do valor de: R$%.2f, Realizado" % valor)
                        print("O Valor da taxa de 3%% do seu Saque foi: R$%.2f" % taxa)
                        print()
                        print("Seu novo saldo é de: R$%.2f" % dicio['saldo'])
                        print()
                        
                        newOp(cnpj, '-', valor, dicio['saldo'], taxa) # Salva a operação no extrato
                        
                        break
                    else:
                        print()
                        print("Essa operação excede o valor minímo de saldo do seu tipo de conta")
                        print()
                        
                        break
            else:
                print()
                print('Senha Inválida')
                print()
        else:
            verif = True
    
    if verif:
        print()
        print("CNPJ não encontrado")
        print()

    save()

    
#5. Depósito
def deposito():
    verif = False
    print()
    print("Digite seus dados para realizar o débito em conta:")
    print()

    while (True):
        try:
            cnpj = int(input("Digite o CNPJ: "))
            break
        except ValueError:
            print("CNPJ Inválido")
    
    ret(cnpj)
    # abre a lista e aumenta o saldo com base no valor do depósito após verificar a senha e O CNPJ
    for dicio in lista_clientes:
        if dicio['cnpj'] == cnpj:
            verif = False
            senha = input("Senha: ")
            ret(senha)
            if dicio['senha'] == senha:
                print()
                print("Saldo em conta: %.2f" % dicio['saldo'])
                while (True):
                    try:
                        valor = float(input("Valor do depósito: "))
                        verifValue(valor)
                        break
                        
                    except ValueError:
                        print("Valor Inválido")
                ret(valor)
                dicio['saldo'] += valor

                print()
                print("Depósito do valor de: R$%.2f, Realizado" % valor)
                print()
                print("Seu novo saldo é de: R$%.2f" % dicio['saldo'])
                print()
                
                newOp(cnpj, '+', valor, dicio['saldo']) # Salva a operação no extrato
                
                break
            else:
                print()
                print('Senha Inválida')
                print()
        else:
            verif = True
    
    if verif:
        print()
        print("CNPJ não encontrado")
        print()

    save()

#6. Extrato
def extrato():
    print()
    print("Digite seus dados para ver o extrato:")
    print()
    
    while (True):
        try:
            cnpj = int(input("Digite o CNPJ: "))
            break
        except ValueError:
            print("CNPJ Inválido")
            
    ret(cnpj)
    
    #Abre a lista e acha o cliente para printar cada linha de str presente na lista de extrato
    for dicio in lista_clientes:
        if dicio['cnpj'] == cnpj:
            senha = input("Senha: ")
            ret(senha)
            verif = False
            if dicio['senha'] == senha:
                print()
                for linha in dicio['extrato']:
                    print(linha)
                print()
                
                break
            else:
                print()
                print('Senha Inválida')
                print()
        else:
            verif = True
    
    if verif:
        print()
        print("CNPJ não encontrado")
        print()
    

#7. Transferência entre contas
def transferencia():
    verif = False #
    verif2 = False #
    print()
    print("Digite seus dados para realiar a transferência:")
    print()
    
    while (True):
        try:
            cnpj = int(input("Digite o CNPJ: "))
            break
        except ValueError:
            print("CNPJ Inválido")
            
    ret(cnpj)


    for dicio in lista_clientes:
        if dicio['cnpj'] == cnpj:
            verif = False
            senha = input("Senha: ")
            ret(senha)
            if senha == dicio['senha']:
                while (True):
                    try:
                        cnpj2 = int(input("Digite o CNPJ do Destinatário: "))
                        if cnpj2 == cnpj:
                            print("CNPJ Inválido")
                            return
                        else:
                            break  
                    except ValueError:
                        print("CNPJ Inválido")
                
                ret(cnpj2)
                
                for dicio2 in lista_clientes:
                    if dicio2['cnpj'] == cnpj2:
                        verif2 = False
                        print()
                        print("Seu saldo é de: R$%.2f" % dicio['saldo'])
                        print()
                        while (True):
                            try:
                                valor = float(input("Digite o Valor da Transferência: "))
                                verifValue(valor)
                                break
                                
                            except ValueError:
                                print("Valor Inválido")
                        ret(valor)
                        # verifica qual o valor da conta para saber se a operação pode ser realizada
                        if dicio['tipoConta'] == 'Comum':
                            if dicio['saldo'] - valor >= -1000:
                                dicio['saldo'] -= valor
                                dicio2['saldo'] += valor

                                print()
                                print("Transferência do valor de: R$%.2f, realizada com sucesso!" % valor)
                                print()
                                print("Seu novo saldo é de: R$%.2f" % dicio['saldo'])
                                print()
                                
                                newOp(cnpj, '-', valor, dicio['saldo']) # Salva a operação no extrato da conta remetente
                                newOp(cnpj2, '+', valor, dicio2['saldo']) # Salva a operação no extrato da conta destinatária
                                
                                verif3 = True
                                break
                            else:
                                print()
                                print("Essa operação excede o valor minímo de saldo do seu tipo de conta.")
                                print()
                                
                                verif3 = True
                                break
                            
                        else:
                            if dicio['saldo'] - valor >= -5000:
                                dicio['saldo'] -= valor
                                dicio2['saldo'] += valor
                                
                                print()
                                print("Transferência do valor de: R$%.2f, realizada com sucesso!" % valor)
                                print()
                                print("Seu novo saldo é de: R$%.2f" % dicio['saldo'])
                                print()
                                
                                newOp(cnpj, '-', valor, dicio['saldo'])
                                newOp(cnpj2, '+', valor, dicio2['saldo'])

                                verif3 = True
                                break
                            else:
                                print()
                                print("Essa operação excede o valor minímo de saldo do seu tipo de conta")
                                print()
                                
                                verif3 = True
                                break
                    else:
                        verif2 = True
                        
                if verif3: # verifica se a operação foi realizada para quebrar o primeiro for
                    break
                if verif2: #printa e cancela a operação se o segundo cnpj não for encontrado
                    print()
                    print("CNPJ não encontrado")
                    print()
                    
                    break
            else: #printa e cancela a operação se a senha não for correta
                print()
                print('Senha Inválida')
                print()
                
                break
        else:
            verif = True
    

    if verif: #printa e cancela a operação se o primeiro cnpj não for encontrado
        print()
        print("CNPJ não encontrado")
        print()
    

    save()

#8. Pagamento de Funcionários
def pagFuncionarios():
    verif = False
    while (True):
        try:
            cnpj = int(input("Digite seu CNPJ para continuar: "))
            break
        except ValueError:
            print("CNPJ Inválido")
            
    ret(cnpj)

    #Abre a lista de clientes e para acessar os dados da conta
    for dicio in lista_clientes:
        if dicio['cnpj'] == cnpj:
            verif = False
            senha = input("Senha: ")
            if senha == dicio['senha']:

                soma = 0
                print()
                print("Digite o valor dos salários dos funcionários.")
                print("Quando terminar digite 0")
                print()
                # Inicia uma repetição para ver o valor do salário de cada funcionário e é encerrado quando édigitado 0
                while(True):
                    while (True):
                        try:
                            salario = float(input("Digite o valor do salário do funcionário: "))
                            verifValue(salario)
                            break
                            
                        except ValueError:
                            print("Valor Inválido")
                    if salario == 0:
                        break
                    soma += salario

                # Verifica o tipo de conta para não passar do valor minimo e realiza a operação
                while(True):
                    if dicio['tipoConta'] == 'Comum':
                        if dicio['saldo'] - soma >= -1000:
                            confirm = input("Deseja fazer o debito para pagamento de funcionários no valor de: R$%.2f? (s/n) " % soma) # Confirma se quer realizar o débito do valor total dos salários
                            if confirm == 's':
                                dicio['saldo'] -= soma
                                print()
                                print("Pagamento realizado com sucesso!")
                                print()
                                newOp(cnpj, '-', soma, dicio['saldo'])
                                save()
                                break
                            elif confirm == 'n':
                                print()
                                print("Operação cancelada.")
                                print()
                                break
                            else:
                                print("Opção Inválida")
                        else:
                            print()
                            print("Essa operação excede o valor minímo de saldo do seu tipo de conta")
                            print()
                            
                            break
                    else:
                        if dicio['saldo'] - soma >= -5000:
                            confirm = input("Deseja fazer o debito para pagamento de funcionários no valor de: R$%.2f? (s/n) " % soma)
                            if confirm == 's':
                                dicio['saldo'] -= soma
                                print()
                                print("Pagamento realizado com sucesso!")
                                print()
                                newOp(cnpj, '-', soma, dicio['saldo'])
                                save()
                                break
                            elif confirm == 'n':
                                print()
                                print("Operação cancelada.")
                                print()
                                break
                            else:
                                print("Opção Inválida")
                        else:
                            print()
                            print("Essa operação excede o valor minímo de saldo do seu tipo de conta")
                            print()
                            
                            break
                            
                break
            else:
                print("Senha incorreta.")
                break
        else:
            verif = True

    if verif:
        print()
        print("CNPJ não encontrado")
        print()

#Menu
while(True):
    print('Menu de Opções:')
    print()
    print("""1. Novo cliente
2. Apaga cliente
3. Listar clientes
4. Débito
5. Depósito
6. Extrato
7. Transferência entre contas
8. Pagamento de Funcionários
9. Sair""")
    print()
    print("Obs.: Para retornar ao menu de opções após entrar em alguma das opções digite 0 em qualquer entrada.\n")
    
    opcao = str(input("Digite o número da opção desejada: "))
    if opcao == '1':
        print()
        try:
            newClient()
        except Exception as x: # Se uma excessão dentro da função for pega é printada como cancelamento
            retMenu(x)
        
    elif opcao == '2':
        print()
        try:
            delClient()
        except Exception as x:
            retMenu(x)
        
    elif opcao == '3':
        print()
        clientList()
    
    elif opcao == '4':
        print()
        try:
            saque()
        except Exception as x:
            retMenu(x)
        
    elif opcao == '5':
        print()
        try:
            deposito()
        except Exception as x:
            retMenu(x)
        
    elif opcao == '6':
        print()
        try:
            extrato()
        except Exception as x:
            retMenu(x)
        
    elif opcao == '7':
        print()
        try:
            transferencia()
        except Exception as x:
            retMenu(x)
        
    elif opcao == '8':
        print()
        try:
            pagFuncionarios()
        except Exception as x:
            retMenu(x)

    elif opcao == '9':
        break
    
    else:
        print("Opção inválida")