import sqlite3
import os
import re

conexao = sqlite3.connect("contatos.db")
cursor = conexao.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS contatos (nome TEXT, telefone TEXT, email TEXT)")

agenda = []

class Contato:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email

cursor.execute("SELECT * FROM contatos ORDER BY nome COLLATE NOCASE")
contatos = cursor.fetchall()
for i in range(0, len(contatos)):
    contato = Contato(contatos[i][0], contatos[i][1], contatos[i][2])
    agenda.append(contato)

padrao = r"[a-zA-Z0-9]+(\.)?(_)?([a-zA-Z0-9]+)?@[a-zA-Z0-9]+\.com(\.br)?"

def atualizar_agenda(cursor):
    
    agenda.clear()
    cursor.execute("SELECT * FROM contatos ORDER BY nome COLLATE NOCASE")
    contatos = cursor.fetchall()
    for i in range(0, len(contatos)):
        contato = Contato(contatos[i][0], contatos[i][1], contatos[i][2])
        agenda.append(contato)

def adicionar_contato(cursor, agenda, conexao, padrao):

    os.system('cls')
    while True:
        print ("[AGENDA DE CONTATOS]:")
        print ("")
        nome = input("[CONTATO]:")
        telefone = input("[TELEFONE]:")
        email = input("[EMAIL]:")
        dup = False
        dupEmail = False
        for i in range(0, len(agenda)):
            if telefone == agenda[i].telefone:
                dup = True
            if email == agenda[i].email:
                dupEmail = True
                break
        os.system('cls')
        if re.fullmatch(padrao , email) == None:
            print ("[ERROR]: Email inválido!")
        if dupEmail == True:
            print ("[ERROR]: O email [" + email + "] já foi cadastrado. Tente Novamente!")
        if dup == True:
            print("[ERROR]: Número de telefone já foi cadastrado! Tente Novamente.")
            print ("")
        if len(telefone) != 11:
            print("[ERROR]: Este número de telefone tem menos de 11 dígitos!")
            print ("")
        if not telefone.isdigit():
            print ("[ERROR]: Use apenas números para digitar o telefone!")
            print ("")
        elif dup == False and telefone.isdigit() and len(telefone) == 11 and dupEmail == False and re.fullmatch(padrao , email) != None:
            contato = Contato(nome, telefone, email)
            agenda.append(contato)
            cursor.execute("INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone, email))
            conexao.commit()
            while True:
                print ("")
                print ("[CONTATO]:", nome, "[TELEFONE]:", telefone + ".")
                print ("[EMAIL]:", email)
                print ("[CADASTRO DE CONTATO REALIZADO COM SUCESSO!]")
                print ("")
                resp = input ("Deseja continuar? [S/N]")
                if resp.upper() == "N":
                    os.system('cls')
                    return
                elif resp.upper() == "S":
                    os.system('cls')
                    break
                elif resp.upper() != "S" and resp.upper() != "N":
                    os.system('cls')
                    print ("")
                    print ("[ERROR]: Escolha as opções correspondentes!")
                    print ("")

def agenda_Decontatos(agenda):

    while True:
        os.system('cls')
        print("[AGENDA DE CONTATOS]:")
        print("")
        print("[CONTATOS CADASTRADOS]:")
        print("")
        for i in range(0, len(agenda)):
            print("[NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
            print ("· [EMAIL]:", agenda[i].email)
            print("")
        resp = input("Deseja voltar ao menu? [S/N]")
        if resp.upper() == "N":
            os.system('cls')
            print("[DESCONECTADO]")
            return True
        elif resp.upper() == "S":
            os.system('cls')
            return
        elif resp.upper() != "S" and resp.upper() != "N":
            os.system('cls')

def remover_contato(agenda, cursor, conexao):

    os.system('cls')
    while True:
        if agenda:
            print("[REMOÇÃO DE CONTATOS]")
            print("")
            for i in range(0, len(agenda)):
                print("[" + str(i + 1) + "º] [CONTATO]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                print ("· [EMAIL]:", agenda[i].email)
                print ("")
            print("[REMOÇÃO DE CONTATO]")
            print ("")
            resp = input ("Deseja remover um contato? [S/N]")
            if resp.upper() == "S":
                cont = 0
                for i in range(0, len(agenda)):
                    cont = cont + 1
                print ("")
                print ("[CONTATOS ENCONTRADOS]: (" + str(cont) + ")")
                print ("")
                print("[AVISO]: Digite apenas o número do contato correspondente. Insira um número de 1 a", str(cont) + ".")
                remove = input ("[Escolha a opção correspondente]:")
                if remove.isdigit() and 1 <= int(remove) <= len(agenda):
                    indice = int(remove) - 1
                    nome = agenda[indice].nome
                    telefone = agenda[indice].telefone
                    email = agenda[indice].email
                    print("")
                    while True:
                        resp = input ("Tem certeza que deseja apagar este contato? Esta ação não pode ser desfeita. [S/N]")
                        if resp.upper() == "N":
                            os.system('cls')
                            return
                        elif resp.upper() == "S":
                            print("")
                            while True:
                                resp = input("[REMOVER CONTATO]: [" + nome + "] TELEFONE: [" + telefone + "] EMAIL: ["+ email +"] ? [S/N]")
                                if resp.upper() == "N":
                                    os.system('cls')
                                    return
                                elif resp.upper() == "S":
                                    agenda.pop(indice)
                                    cursor.execute("DELETE FROM contatos WHERE telefone = ?", (telefone,))
                                    conexao.commit()
                                    print ("")
                                    while True:
                                        print("[CONTATO EXCLUÍDO]")
                                        print("")
                                        resp = input("Deseja voltar ao menu? [S/N]")
                                        if resp.upper() == "S":
                                            os.system('cls')
                                            return
                                        elif resp.upper() == "N":
                                            os.system('cls')
                                            print ("[DESCONECTADO]")
                                            return True
                                        elif resp.upper() != "N" and resp.upper() != "S":
                                            os.system('cls')
                                elif resp.upper() != "N" and resp.upper() != "S":
                                    os.system('cls')
                        elif resp.upper() != "S" and resp.upper() != "N":
                            os.system('cls')
                else:
                    os.system('cls')
                    print ("")
                    print("[ERROR] Contato inválido! Tente Novamente.")
                    print ("")
            elif resp.upper() == "N":
                os.system('cls')
                return
            elif resp.upper() != "S" and resp.upper() != "N":             
                os.system('cls')
        else:
            print ("")
            print("[ERROR] Nenhum contato cadastrado!")
            print ("")
            return

def busca_de_contato(agenda):

    while True:
        
        os.system('cls')
        print ("[BUSCA DE CONTATOS]")
        print ("")
        print ("[1] Busca por nome.")
        print ("[2] Busca por inicial.")
        print ("[3] Busca por email.")
        print ("[0] Sair")
        op2 = input ("[ESCOLHA AS OPÇÕES CORRESPONDENTES]:")

        match op2:

            case "1":

                sair = False
                while sair == False:
                    
                    os.system('cls')
                    print ("[BUSCA POR NOME]")
                    print ("")
                    encontrarNome = input("[NOME]:")
                    nomeEncontado = []
                    telefoneEncontado = []
                    emailEncontrado = []
                    contatoInexistente = True
                    for i in range(0, len(agenda)):
                        if encontrarNome.upper() == agenda[i].nome.upper():
                            contatoInexistente = False
                            nomeEncontado.append(agenda[i].nome)
                            telefoneEncontado.append(agenda[i].telefone)
                            emailEncontrado.append(agenda[i].email)
                    if contatoInexistente == False:
                        while True:
                            print("")
                            print("[CONTATO(s) ENCONTRADO(s)]: (" + str(len(nomeEncontado)) + ")")
                            print("[informações do(s) contato(s)]:")
                            print ("")
                            for i in range(0, len(nomeEncontado)):
                                print ("[NOME DE CONTATO]:", nomeEncontado[i] + ".")
                                print ("[TELEFONE]: (" + telefoneEncontado[i] + ")")
                                print ("[E-MAIL]: (" + emailEncontrado[i] + ")")
                                print("")
                            resp = input("Deseja continuar? [S/N]")
                            if resp.upper() == "N":
                                sair = True
                                break
                            elif resp.upper() == "S":
                                break
                            elif resp.upper() != "N" and resp.upper() != "S":
                                os.system('cls')
                    if contatoInexistente == True:
                        while True:
                            print("")
                            print("[ERROR]: CONTATO NÃO ENCONTRADO!")
                            print ("")
                            resp = input("Deseja continuar? [S/N]")
                            if resp.upper() == "N":
                                sair = True
                                break
                            elif resp.upper() == "S":
                                break
                            elif resp.upper() != "N" and resp.upper() != "S":
                                os.system('cls')

            case "2":

                sair = False
                while sair == False:
                    
                    os.system('cls')
                    print ("[BUSCA POR INICIAL]")
                    print ("")
                    buscaInicial = input("[Digite uma letra]:")
                    print ("")
                    contatos = []
                    telefones = []
                    emails = []
                    verificao = False
                    if len(buscaInicial) == 1:
                        for i in range(0, len(agenda)):
                            if buscaInicial.upper()[0] == agenda[i].nome.upper()[0]:
                                verificao = True
                                contatos.append(agenda[i].nome)
                                telefones.append(agenda[i].telefone)
                                emails.append(agenda[i].email)
                        if verificao == True:
                            while True:
                                print ("[CONTATO(s) ENCONTRADO(s)]: (" + str(len(contatos)) + ")")
                                print("[informações do(s) contato(s)]:")
                                print ("")
                                for i in range(0, len(contatos)):
                                    print ("[NOME DE CONTATO]:", contatos[i], "[TELEFONE]: (" + telefones[i] + ")")
                                    print ("[E-MAIL]: (" + emails[i] + ")")
                                    print ("")
                                resp = input("Deseja continuar? [S/N]")
                                if resp.upper() == "N":
                                    sair = True
                                    break
                                elif resp.upper() == "S":
                                    break
                                elif resp.upper() != "N" and resp.upper() != "S": 
                                    os.system('cls')
                        else:
                            while True:
                                print ("[ERROR]: Nenhum contato com a letra [" + buscaInicial + "] foi encontrada!")
                                print("")
                                resp = input("Deseja continuar? [S/N]")
                                if resp.upper() == "N":
                                    sair = True
                                    break
                                elif resp.upper() == "S":
                                    break
                                elif resp.upper() != "N" and resp.upper() != "S":
                                    os.system('cls')
                    if len(buscaInicial) > 1 and buscaInicial.isalpha():   
                        while True:
                            print ("[WARN]: Digite apenas uma letra para achar os contatos correspondentes!")
                            print ("")
                            resp = input("Ainda deseja continuar? [S/N]")
                            if resp.upper() == "N":
                                sair = True
                                break
                            elif resp.upper() == "S":
                                break
                            elif resp.upper() != "N" and resp.upper() != "S":
                                os.system('cls')

            case "3":

                os.system('cls')

                sair = False
                while sair == False:
                        print ("[BUSCA POR E-MAIL]")
                        print ("")
                        print ("[WARN]: Digite parte do E-mail!")
                        buscaEmail = input("[E-Mail]:")
                        if buscaEmail == "":
                            os.system('cls')
                            print ("[ERROR]: O usúario precisa digitar o e-mail!")
                            print ("")
                        else:
                            contatos = []
                            telefones = []
                            emails = []
                            verificao = False
                            for i in range(0, len(agenda)):
                                if buscaEmail.upper() in agenda[i].email.upper():
                                    verificao = True
                                    contatos.append(agenda[i].nome)
                                    telefones.append(agenda[i].telefone)
                                    emails.append(agenda[i].email)
                            if verificao == True:
                                while True:
                                    print ("")
                                    print ("[CONTATO(s) ENCONTRADO(s)]: (" + str(len(contatos)) + ")")
                                    print("[informações do(s) contato(s)]:")
                                    print ("")
                                    for i in range(0, len(contatos)):
                                        print ("[NOME DE CONTATO]:", contatos[i], "[TELEFONE]: (" + telefones[i] + ")")
                                        print ("[E-MAIL]: (" + emails[i] + ")")
                                        print ("")
                                    resp = input("Deseja continuar? [S/N]")
                                    if resp.upper() == "N":
                                        os.system('cls')
                                        sair = True
                                        break
                                    elif resp.upper() == "S":
                                        os.system('cls')
                                        break
                                    elif resp.upper() != "N" and resp.upper() != "S": 
                                        os.system('cls')
                            else:
                                while True:
                                    print ("[ERROR]: Nenhum contato com o email digitado [" + buscaEmail + "] foi encontrado!")
                                    print("")
                                    resp = input("Deseja continuar? [S/N]")
                                    if resp.upper() == "N":
                                        os.system('cls')
                                        sair = True
                                        break
                                    elif resp.upper() == "S":
                                        os.system('cls')
                                        break
                                    elif resp.upper() != "N" and resp.upper() != "S":
                                        os.system('cls')
            
            case _:
                if op2 != "0":
                    os.system('cls')
                else:
                    os.system('cls')
                    return

def ordenacao_alfabetica(agenda):

    while True:
        os.system('cls')
        print ("[ORDENAÇÃO ALFABÉTICA]")
        print ("")
        print ("[WARN]: Isso irá fazer com que seus contatos fiquem em ordem alfabética!")
        resp = input("Deseja fazer altereções na sua agenda? [S/N]")
        if resp.upper() == "N":
            os.system('cls')
            return
        elif resp.upper() == "S":
            agenda.sort(key = lambda n: n.nome.upper())
            print ("")
            while True:
                print ("[AGENDA ALTERADA COM SUCESSO!]")
                resp = input ("Deseja ver a lista de contatos atualizada? [S/N]")
                if resp.upper() == "N":
                    os.system('cls')
                    return
                elif resp.upper() == "S":
                    print ("")
                    while True:
                        print ("[LISTA DE CONTATOS]")
                        print ("")
                        for i in range(0, len(agenda)):
                            print("[CONTATO", str(i + 1) + "]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                        print ("")
                        resp = input("Deseja voltar ao menu? [S/N]")
                        if resp.upper() == "N":
                            os.system('cls')
                            print("[DESCONECTADO]")
                            return True
                        elif resp.upper() == "S":
                            os.system('cls')
                            return
                        elif resp.upper() != "N" and resp.upper() != "S": 
                            os.system('cls')
                elif resp.upper() != "N" and resp.upper() != "S":
                    os.system('cls')
        elif resp.upper() != "N" and resp.upper() != "S":
            os.system('cls')

def edicao_contato(cursor, conexao, padrao, agenda):

    os.system('cls')
    while True:
        print("[EDIÇÃO DE CONTATOS]:")
        print ("")
        print ("[1] Edição de nome.")
        print ("[2] Edição de telefone.")
        print ("[3] Edição de e-mail.")
        print ("[0] Sair")
        op = input("Escolha a opção correspondente:")

        match op:

            case "1":
                
                os.system('cls')
                while True:
                    print("[EDIÇÃO DE NOME]:")
                    print("")
                    print("[CONTATOS CADASTRADOS]:")
                    print("")
                    for i in range(0, len(agenda)):
                        print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                        print ("· [EMAIL]:", agenda[i].email)
                        print ("")
                    resp = input("Deseja editar de algum contato existente? [S/N]")
                    if resp.upper() == "N":
                        os.system('cls')
                        return
                    elif resp.upper() == "S":
                        while True:
                            print ("")
                            print ("[EDIÇÃO DE NOME]")
                            encontrarNome = input("[Número de contato correspondente]:")
                            if not encontrarNome.isdigit():
                                os.system('cls')
                                print ("[ERROR]: Digite apenas números!")
                                print ("")
                                for i in range(0, len(agenda)):
                                    print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                                    print ("· [EMAIL]:", agenda[i].email)
                                    print ("")
                            try:
                                if int(encontrarNome) > len(agenda):
                                    os.system('cls')
                                    print ("[ERROR]: O número digitado é invalido. Tente Novamente!")
                                    print ("")
                                    for i in range(0, len(agenda)):
                                        print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                                        print ("· [EMAIL]:", agenda[i].email)
                                        print ("")
                            except:
                                pass
                            if encontrarNome.isdigit() and 1 <= int(encontrarNome) <= len(agenda):
                                indice = encontrarNome
                                indice = int(indice) - 1
                                contato = agenda[indice].nome
                                telefone = agenda[indice].telefone
                                email = agenda[indice].email
                                break
                        while True:
                                print ("")
                                print ("[CONTATO]:", contato, "[TELEFONE]:", telefone + ".")
                                print ("[EMAIL]:", email)
                                print ("")
                                resp = input("Deseja realmente alterar o nome desse contato? [S/N]")
                                if resp.upper() == "N":
                                    os.system('cls')
                                    return
                                elif resp.upper() == "S":
                                    print ("")
                                    while True:
                                        editarNome = input ("[NOVO NOME]:")
                                        print ("")
                                        cursor.execute("UPDATE contatos SET nome = ? WHERE telefone = ?", (editarNome, agenda[indice].telefone))
                                        conexao.commit()
                                        print("[NOME ALTERADO]")
                                        print("")
                                        while True:
                                            resp = input("Deseja voltar ao menu? [S/N]")
                                            if resp.upper() == "S":
                                                os.system('cls')
                                                return
                                            elif resp.upper() == "N":
                                                os.system('cls')
                                                print ("[DESCONECTADO]")
                                                return True
                                            elif resp.upper() != "N" and resp.upper() != "S":
                                                os.system('cls')
                                            
                                elif resp.upper() != "N" and resp.upper() != "S":
                                    os.system('cls')
                    elif resp.upper() != "N" and resp.upper() != "S":
                        os.system('cls')  

            case "2":

                os.system('cls')
                while True:
                    print("[EDIÇÃO DE TELEFONE]:")
                    print("")
                    print("[CONTATOS CADASTRADOS]:")
                    print("")
                    for i in range(0, len(agenda)):
                        print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                        print ("· [EMAIL]:", agenda[i].email)
                        print ("")
                    resp = input("Deseja editar de algum contato existente? [S/N]")
                    if resp.upper() == "N":
                        os.system('cls')
                        return
                    elif resp.upper() == "S":
                        while True:
                            print ("")
                            print ("[EDIÇÃO DE TELEFONE]")
                            encontrarTelefone = input("[Número de contato correspondente]:")
                            if not encontrarTelefone.isdigit():
                                os.system('cls')
                                print ("[ERROR]: Digite apenas números!")
                                print ("")
                                for i in range(0, len(agenda)):
                                    print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                                    print ("· [EMAIL]:", agenda[i].email)
                                    print ("")
                            try:
                                if int(encontrarTelefone) > len(agenda):
                                    os.system('cls')
                                    print ("[ERROR]: O número digitado é invalido. Tente Novamente!")
                                    print ("")
                                    for i in range(0, len(agenda)):
                                        print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                                        print ("· [EMAIL]:", agenda[i].email)
                                        print ("")
                            except:
                                pass
                            if encontrarTelefone.isdigit() and 1 <= int(encontrarTelefone) <= len(agenda):
                                indice = encontrarTelefone
                                indice = int(indice) - 1
                                contato = agenda[indice].nome
                                telefone = agenda[indice].telefone
                                email = agenda[indice].email
                                break
                        while True:
                                print ("")
                                print ("[CONTATO]:", contato, "[TELEFONE]:", telefone + ".")
                                print ("[EMAIL]:", email)
                                print ("")
                                resp = input("Deseja realmente alterar o telefone desse contato? [S/N]")
                                if resp.upper() == "N":
                                    os.system('cls')
                                    return
                                elif resp.upper() == "S":
                                    print ("")
                                    while True:
                                        editarTelefone = input ("[NOVO TELEFONE]:")
                                        print ("")
                                        dup = False
                                        for i in range(0, len(agenda)):
                                            if editarTelefone == agenda[i].telefone:
                                                dup = True
                                        if dup == True:
                                            print("[ERROR]: Número de telefone já foi cadastrado! Tente Novamente.")
                                            print ("")
                                        if len(editarTelefone) < 11:
                                            print("[ERROR]: Este número de telefone tem menos de 11 dígitos!")
                                            print ("")
                                        if len(editarTelefone) > 11:
                                            print("[ERROR]: Este número de telefone tem mais de 11 dígitos!")
                                            print ("")
                                        if not editarTelefone.isdigit():
                                            print ("[ERROR]: Use apenas números para digitar o telefone!")
                                            print ("")
                                        if editarTelefone.isdigit() and len(editarTelefone) == 11 and dup == False:
                                            print ("")
                                            cursor.execute("UPDATE contatos SET telefone = ? WHERE email = ?", (editarTelefone, agenda[indice].email))
                                            conexao.commit()
                                            print("[TELEFONE ALTERADO]")
                                            print("")
                                            while True:
                                                resp = input("Deseja voltar ao menu? [S/N]")
                                                if resp.upper() == "S":
                                                    os.system('cls')
                                                    return
                                                elif resp.upper() == "N":
                                                    os.system('cls')
                                                    print ("[DESCONECTADO]")
                                                    return True
                                                elif resp.upper() != "N" and resp.upper() != "S":
                                                    os.system('cls')
                                            
                                elif resp.upper() != "N" and resp.upper() != "S":
                                    os.system('cls')
                    elif resp.upper() != "N" and resp.upper() != "S":
                        os.system('cls')  

            case "3":

                os.system('cls')
                while True:
                    print("[EDIÇÃO DE EMAIL]:")
                    print("")
                    print("[CONTATOS CADASTRADOS]:")
                    print("")
                    for i in range(0, len(agenda)):
                        print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                        print ("· [EMAIL]:", agenda[i].email)
                        print ("")
                    resp = input("Deseja editar o email de algum email existente? [S/N]")
                    if resp.upper() == "N":
                        os.system('cls')
                        return
                    elif resp.upper() == "S":
                        while True:
                            print ("")
                            print ("[EDIÇÃO DE EMAIL]")
                            encontrarEmail = input("[Número de contato correspondente]:")
                            if not encontrarEmail.isdigit():
                                os.system('cls')
                                print ("[ERROR]: Digite apenas números!")
                                print ("")
                                for i in range(0, len(agenda)):
                                    print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                                    print ("· [EMAIL]:", agenda[i].email)
                                    print ("")
                            try:
                                if int(encontrarEmail) > len(agenda):
                                    os.system('cls')
                                    print ("[ERROR]: O número digitado é invalido. Tente Novamente!")
                                    print ("")
                                    for i in range(0, len(agenda)):
                                        print(str(i + 1) + "º [NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                                        print ("· [EMAIL]:", agenda[i].email)
                                        print ("")
                            except:
                                pass
                            if encontrarEmail.isdigit() and 1 <= int(encontrarEmail) <= len(agenda):
                                indice = encontrarEmail
                                indice = int(indice) - 1
                                contato = agenda[indice].nome
                                telefone = agenda[indice].telefone
                                email = agenda[indice].email
                                break
                        while True:
                                print ("")
                                print ("[CONTATO]:", contato, "[TELEFONE]:", telefone + ".")
                                print ("[EMAIL]:", email)
                                print ("")
                                resp = input("Deseja realmente alterar o email desse contato? [S/N]")
                                if resp.upper() == "N":
                                    os.system('cls')
                                    return
                                elif resp.upper() == "S":
                                    print ("")
                                    while True:
                                        dupEmail = False
                                        editarEmail = input ("[NOVO EMAIL]:")
                                        for i in range(0, len(agenda)):
                                            if editarEmail == agenda[i].email:
                                                dupEmail = True
                                                break
                                        if dupEmail == True:
                                            os.system('cls')
                                            print ("[ERROR]: O email [ " + editarEmail + " ] já foi cadastrado. Tente Novamente!")
                                            print ("")
                                        if re.fullmatch(padrao , editarEmail) == None:
                                            os.system("cls")
                                            print ("[ERROR]: Email inválido!")
                                            print ("")
                                            print ("""Como escrever o e-mail
                                            
O e-mail precisa seguir este formato.
                                            
1. Começa com letras ou números.
2. Pode ter um ponto ou um underscore no meio, mas só um de cada.
3. Depois vem o @.
4. Em seguida o nome do site, com letras ou números.
5. Termina em .com ou .com.br.
                                            
Exemplos aceitos: rogerio@gmail.com, joao.silva@gmail.com, maria_souza@empresa.com.br
                                            
Exemplos recusados: rogerio@@gmail.com, rogerio@gmail.org""")
                                            print ("")
                                        if dupEmail == False and re.fullmatch(padrao , editarEmail) != None:
                                            cursor.execute("UPDATE contatos SET email = ? WHERE telefone = ?", (editarEmail, agenda[indice].telefone))
                                            conexao.commit()
                                            print ("")
                                            print("[EMAIL ALTERADO]")
                                            print("")
                                            while True:
                                                resp = input("Deseja voltar ao menu? [S/N]")
                                                if resp.upper() == "S":
                                                    os.system('cls')
                                                    return
                                                elif resp.upper() == "N":
                                                    os.system('cls')
                                                    print ("[DESCONECTADO]")
                                                    return True
                                                elif resp.upper() != "N" and resp.upper() != "S":
                                                    os.system('cls')
                                            
                                elif resp.upper() != "N" and resp.upper() != "S":
                                    os.system('cls')
                    elif resp.upper() != "N" and resp.upper() != "S":
                        os.system('cls')  
            
            case _:
                
                if op != "0":
                    os.system('cls')
                    print ("[ERROR]: Escolha as opções correspondentes!")
                    print ("")
                else:
                    os.system('cls')
                    return

op = 999
while op != "0":

    atualizar_agenda(cursor)
    os.system('cls')
    print ("[MENU]")
    print ("")
    print ("[1] Adicionar contato.")
    print ("[2] Ver agenda de contatos.")
    print ("[3] Remover contatos.")
    print ("[4] Busca de contato.")
    print ("[5] Ordenação alfabética.")
    print ("[6] Edição de contato.")
    print ("[0] Sair.")
    print ("")
    op = input("Escolha a opção correspondente:")

    match op:

        case "1":

            adicionar_contato(cursor, agenda, conexao, padrao)
  
        case "2":

            desconectar = agenda_Decontatos(agenda)
            if desconectar == True:
                op = "0"

        case "3":

            desconectar = remover_contato(agenda, cursor, conexao)
            if desconectar == True:
                op = "0"

        case "4":

            busca_de_contato(agenda)

        case "5":

            desconectar = ordenacao_alfabetica(agenda)
            if desconectar == True:
                op = "0"

        case "6":

            desconectar = edicao_contato(cursor, conexao, padrao, agenda)
            if desconectar == True:
                op = "0"

        case _:
            if op != "0":
                os.system('cls')
                print ("[ERROR]: Escolha as opções correspondentes!")
                print ("")
            else:
                os.system('cls')
                print("[DESCONECTADO]")

conexao.close()