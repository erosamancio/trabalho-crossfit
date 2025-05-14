def menu():
    while True:
        print("\n~~~ MENU DE WODs CROSSFIT ~~~")
        print("1) Adicionar WOD")
        print("2) Visualizar WODs")
        print("3) Editar WOD")
        print("4) Excluir WOD")
        print("0) Sair\n")

        opcao = int(input("Digite um numero: "))

        if opcao == "1":
            add()
        elif opcao == "2":
            ver()
        elif opcao == "3":
            edit()
        elif opcao == "4":
            apagar()
        elif opcao == "0":
            print("programa encerrado")
            break
        else:
            print("opção inválida")

def add():
    print("\n--- Novo WOD ---")
    # pegando os dados do usuário
    d = input("Data: ")
    t = input("Tipo: ").upper()  # deixar maiúsculo pra ficar mais padronizado
    s = input("Séries: ")
    r = input("Repetições: ")
    m = input("Movimentos (virgula): ")

    try:
        f = open("wods.txt", "a")  # abre o arquivo no modo adicionar
        f.write(d + ";" + t + ";" + s + ";" + r + ";" + m + "\n")  # escrevendo tudo numa linha só
        f.close()
        print("Salvo!\n")
    except:
        print("deu erro pra salvar")  # caso der algum erro na hora de salvar
def ver():
    print("\n-- WODs --")
    try:
        f = open("wods.txt")  # só abre o arquivo pra ler
        dados = f.readlines()  # le todas as linhas
        f.close()
    except:
        print("erro abrindo o arquivo")
        return

    if dados == []:
        print("não tem nada ainda")  # se o arquivo estiver vazio
        return

    for l in dados:
        # separando as infos pelo ;
        campos = l.split(";")
        print("Data:", campos[0])
        print("Tipo:", campos[1])
        print("Séries:", campos[2])
        print("Repetições:", campos[3])
        print("Movimentos:", campos[4])
        print("------------------")

def edit():
    print("\n--- Editar WOD ---")
    try:
        arq = open("wods.txt", "r")
        todos = arq.readlines()
        arq.close()
    except:
        print("erro abrindo o arquivo")
        return

    if len(todos) == 0:
        print("nada para editar")  # se não tiver nenhum wod
        return

    ver()  # mostra os wods primeiro
    alvo = input("Data do WOD que quer mudar: ")

    novo = ""
    achei = False

    for l in todos:
        c = l.split(";")
        if c[0] == alvo:
            achei = True
            print("1) Tipo\n2) Séries\n3) Repetições\n4) Movimentos")
            esc = input("Qual quer mudar: ")

            # muda só o que a pessoa quiser
            if esc == "1":
                c[1] = input("Novo tipo: ").upper()
            elif esc == "2":
                c[2] = input("Nova série: ")
            elif esc == "3":
                c[3] = input("Nova repetição: ")
            elif esc == "4":
                c[4] = input("Novos movimentos: ") + "\n"
            else:
                print("número errado")
                return

            linha_nova = c[0] + ";" + c[1] + ";" + c[2] + ";" + c[3] + ";" + c[4]
            novo += linha_nova
        else:
            novo += l  # mantém os outros como estavam

    try:
        a = open("wods.txt", "w")
        a.write(novo)  # sobrescreve tudo com as mudanças
        a.close()
    except:
        print("erro ao escrever")
        return

    if achei:
        print("editado com sucesso")
    else:
        print("nada encontrado com essa data")

def apagar():
    print("\n--- Apagar WOD ---")
    try:
        f = open("wods.txt", "r")
        linhas = f.readlines()
        f.close()
    except:
        print("erro no arquivo")
        return

    if linhas == []:
        print("não tem nada pra apagar")
        return

    ver()
    data = input("Digite a data pra apagar: ")

    novo = ""
    achou = False

    for l in linhas:
        pedacos = l.split(";")
        if pedacos[0] != data:
            novo += l
        else:
            achou = True  # achou o wod que quer apagar

    try:
        f = open("wods.txt", "w")
        f.write(novo)
        f.close()
    except:
        print("erro ao salvar novo arquivo")
        return

    if achou:
        print("apagado com sucesso")
    else:
        print("não achei esse WOD")

def filtrar():
    print("\n--- Filtrar WODs ---")
    print("1) Por tipo")
    print("2) Por movimento")
    esc = input("Selecione uma opção: ")

    try:
        f = open("wods.txt", "r")
        dados = f.readlines()
        f.close()
    except:
        print("Falha na tentativa de abrir o arquivo")
        return

    if dados == []:
        print("Nenhum WOD cadastrado")
        return

    filtro = input("Digite o que deseja buscar: ").upper()
    encontrou = False

    for l in dados:
        c = l.strip().split(";")
        if esc == "1" and filtro in c[1].upper():
            encontrou = True
        elif esc == "2" and filtro in c[4].upper():
            encontrou = True
        else:
            continue

        if encontrou:
            print("\nData:", c[0])
            print("Tipo:", c[1])
            print("Séries:", c[2])
            print("Repetições:", c[3])
            print("Movimentos:", c[4])
            print("------------------")
            encontrou = False  # reseta pra poder verificar o próximo

    if not encontrou:
        print("Nenhum resultado foi encontrado com esse filtro.")

import os

def checar_arquivo():
    if not os.path.exists("wods.txt"):
        with open("wods.txt", "w") as f:
            pass  # só cria o arquivo vazio
    
def menu():
    checar_arquivo()  # garante que o arquivo existe antes de tudo
    while True:
        print("\n~~ MENU DE WODs CROSSFIT ~~")
        print("1) Adicionar WOD")
        print("2) Visualizar WODs")
        print("3) Editar WOD")
        print("4) Excluir WOD")
        print("5) Filtrar WODs")
        print("0) Sair\n")

        try:
            opcao = int(input("Digite um numero: "))
        except:
            print("Digite apenas números!")
            continue

        if opcao == 1:
            add()
        elif opcao == 2:
            ver()
        elif opcao == 3:
            edit()
        elif opcao == 4:
            apagar()
        elif opcao == 5:
            filtrar()
        elif opcao == 0:
            print("Programa encerrado!")
            break
        else:
            print("Opção inválida")
menu()
