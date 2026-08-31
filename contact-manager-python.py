import sqlite3
import os

conexao = sqlite3.connect("contatos.db")
cursor = conexao.cursor()

try:
    cursor.execute("CREATE TABLE contatos (telefone TEXT, nome TEXT)")
except sqlite3.OperationalError:
    pass

agenda = []

class Contato:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

cursor.execute("SELECT * FROM contatos ORDER BY nome COLLATE NOCASE")
contatos = cursor.fetchall()
for i in range(0, len(contatos)):
    contato = Contato(contatos[i][1], contatos[i][0])
    agenda.append(contato)

def adicionar_contato(cursor, agenda, conexao):

    os.system('cls')
    while True:
        print ("[AGENDA DE CONTATOS]:")
        print ("")
        nome = input("[CONTATO]:")
        telefone = input("[TELEFONE]:")
        dup = False
        for i in range(0, len(agenda)):
            if telefone == agenda[i].telefone:
                dup = True
                break
        if dup == True or len(telefone) != 11 or not telefone.isdigit():
            os.system('cls')
            print("[ERROR]: Número de telefone já foi cadastrado ou é inválido! Tente Novamente.")
            print ("")
        elif dup == False and telefone.isdigit() and len(telefone) == 11:
            contato = Contato(nome, telefone)
            agenda.append(contato)
            cursor.execute("INSERT INTO contatos (telefone, nome) VALUES (?, ?)", (telefone, nome))
            conexao.commit()
            while True:
                print ("")
                print ("[CONTATO]:", nome, "[TELEFONE]:", telefone + ".")
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
                    print ("[ERROR]: Escolha a as opções correspondentes!")
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
                    print("")
                    while True:
                        resp = input ("Tem certeza que deseja apagar este contato? Esta ação não pode ser desfeita. [S/N]")
                        if resp.upper() == "N":
                            os.system('cls')
                            return
                        elif resp.upper() == "S":
                            print("")
                            while True:
                                resp = input("[REMOVER CONTATO]: [" + nome + "] TELEFONE: [" + telefone + "] ? [S/N]")
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
        print ("[1] Busca pro nome.")
        print ("[2] Busca pro inicial")
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
                    contatoInexistente = True
                    for i in range(0, len(agenda)):
                        if encontrarNome.upper() == agenda[i].nome.upper():
                            contatoInexistente = False
                            nomeEncontado.append(agenda[i].nome)
                            telefoneEncontado.append(agenda[i].telefone)
                    if contatoInexistente == False:
                        while True:
                            print("")
                            print("[CONTATO(s) ENCONTRADO(s)]: (" + str(len(nomeEncontado)) + ")")
                            print("[informações do(s) contato(s)]:")
                            print ("")
                            for i in range(0, len(nomeEncontado)):
                                print ("[NOME DE CONTATO]:", nomeEncontado[i] + ".")
                                print ("[TELEFONE]: (" + telefoneEncontado[i] + ")")
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
                    verificao = False
                    if len(buscaInicial) == 1:
                        for i in range(0, len(agenda)):
                            if buscaInicial.upper()[0] == agenda[i].nome.upper()[0]:
                                verificao = True
                                contatos.append(agenda[i].nome)
                                telefones.append(agenda[i].telefone)
                        if verificao == True:
                            while True:
                                print ("[CONTATO(s) ENCONTRADO(s)]: (" + str(len(contatos)) + ")")
                                print("[informações do(s) contato(s)]:")
                                print ("")
                                for i in range(0, len(contatos)):
                                    print ("[NOME DE CONTATO]:", contatos[i], "[TELEFONE]: (" + telefones[i] + ")")
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
                    else:
                        while True:
                            print ("[WARN]: Digite apenas letras para achar os contatos correspondentes!")
                            print ("")
                            resp = input("Ainda deseja continuar? [S/N]")
                            if resp.upper() == "N":
                                sair = True
                                break
                            elif resp.upper() == "S":
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

def edicao_contato(agenda, cursor, conexao):

    os.system('cls')
    while True:
        print("[EDIÇÃO DE CONTATOS]:")
        print("")
        print("[CONTATOS CADASTRADOS]:")
        print("")
        for i in range(0, len(agenda)):
            print("[NOME]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
        print("")
        resp = input("Deseja editar algum contato existente? [S/N]")
        if resp.upper() == "N":
            os.system('cls')
            return
        elif resp.upper() == "S":
            print ("")
            print ("[EDIÇÃO DE CONTATO]")
            encontrarNome = input("[NOME DO CONTATO]:")
            contatoencontrado = False
            for i in range(0, len(agenda)):
                if encontrarNome.upper() == agenda[i].nome.upper():
                    contatoencontrado = True
                    while True:
                        print ("")
                        print ("[CONTATO]:", agenda[i].nome, "[TELEFONE]:", agenda[i].telefone + ".")
                        resp = input("Deseja realmente alterar o nome de contato? [S/N]")
                        if resp.upper() == "N":
                            os.system('cls')
                            return
                        elif resp.upper() == "S":
                            print ("")
                            editarNome = input ("[NOVO NOME]:")
                            agenda[i].nome = editarNome
                            cursor.execute("UPDATE contatos SET nome = ? WHERE telefone = ?", (editarNome, agenda[i].telefone))
                            conexao.commit()
                            os.system('cls')
                            break
                        elif resp.upper() != "N" and resp.upper() != "S":
                            os.system('cls')
            if contatoencontrado == False:
                print ("")
                while True:
                    print ("[ERROR]: CONTATO NÃO ENCONTRADO!")
                    resp = input("Deseja continuar editando? [S/N]")
                    if resp.upper() == "N":
                        os.system('cls')
                        return
                    elif resp.upper() == "S":
                        os.system('cls')
                        break
                    elif resp.upper() != "N" and resp.upper() != "S":
                        os.system('cls')
        elif resp.upper() != "N" and resp.upper() != "S":
            os.system('cls')

op = 999
while op != "0":

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
    
            adicionar_contato(cursor, agenda, conexao)
  
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

            edicao_contato(agenda, cursor, conexao)

        case _:
            if op != "0":
                os.system('cls')
                print ("[ERROR]: Escolha a as opções correspondentes!")
                print ("")
            else:
                os.system('cls')
                print("[DESCONECTADO]")

conexao.close()