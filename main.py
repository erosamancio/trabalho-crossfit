import os
os.system("cls")

def menu():
    checar_arquivo()  # garante que o arquivo de WODs existe
    checar_arquivo_metas()  # garante que o arquivo de metas existe
    while True:
        print("\n~~~ MENU DE WODs CROSSFIT ~~~")
        print("1) Adicionar WOD")
        print("2) Visualizar WODs")
        print("3) Editar WOD")
        print("4) Excluir WOD")
        print("5) Filtrar WODs")
        print("6) Adicionar Meta")
        print("7) Ver Metas")
        print("8) Editar Meta")
        print("9) Sugestão Aleatória de WOD")
        print("10) Conquistas")
        print("0) Sair\n")
        try:
            opcao = int(input("Digite um número: "))
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
        elif opcao == 6:
            add_meta()
        elif opcao == 7:
            ver_metas()
        elif opcao == 8:
            edit_meta()
        elif opcao == 9:
            sugerir_wod()
        elif opcao == 10:
            conquistas()
        elif opcao == 0:
            print("Programa encerrado!")
            break
        else:
            print("Opção inválida")

def checar_arquivo():
    if not os.path.exists("wods.txt"):
        with open("wods.txt", "w") as f:
            pass  # só cria o arquivo vazio

def add():
    print("\n--- Novo WOD ---")
    d = input("Data: ")
    t = input("Tipo: ").upper()
    s = input("Séries: ")
    r = input("Repetições: ")
    m = input("Movimentos (vírgula): ")
    tempo = input("Tempo: ")

    try:
        with open("wods.txt", "a") as f:
            f.write(d + ";" + t + ";" + s + ";" + r + ";" + m + ";" + tempo + "\n")
        print("Salvo!\n")
    except:
        print("Erro ao salvar.")


def ver():
    print("\n-- WODs --")
    try:
        with open("wods.txt") as f:
            dados = f.readlines()
    except:
        print("Erro abrindo o arquivo")
        return

    if not dados:
        print("Não tem nada ainda")
        return

    for l in dados:
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
        with open("wods.txt", "r") as arq:
            todos = arq.readlines()
    except:
        print("Erro abrindo o arquivo")
        return

    if not todos:
        print("Nada para editar")
        return

    ver()
    alvo = input("Data do WOD que quer mudar: ")

    novo = ""
    achei = False

    for l in todos:
        c = l.split(";")
        if c[0] == alvo:
            achei = True
            print("1) Tipo\n2) Séries\n3) Repetições\n4) Movimentos")
            esc = input("Qual quer mudar: ")

            if esc == "1":
                c[1] = input("Novo tipo: ").upper()
            elif esc == "2":
                c[2] = input("Nova série: ")
            elif esc == "3":
                c[3] = input("Nova repetição: ")
            elif esc == "4":
                c[4] = input("Novos movimentos: ") + "\n"
            else:
                print("Número errado")
                return

            linha_nova = c[0] + ";" + c[1] + ";" + c[2] + ";" + c[3] + ";" + c[4]
            novo += linha_nova
        else:
            novo += l

    try:
        with open("wods.txt", "w") as a:
            a.write(novo)
    except:
        print("Erro ao escrever")
        return

    print("Editado com sucesso" if achei else "Nada encontrado com essa data")

def apagar():
    print("\n--- Apagar WOD ---")
    try:
        with open("wods.txt", "r") as f:
            linhas = f.readlines()
    except:
        print("Erro no arquivo")
        return

    if not linhas:
        print("Não tem nada pra apagar")
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
            achou = True

    try:
        with open("wods.txt", "w") as f:
            f.write(novo)
    except:
        print("Erro ao salvar novo arquivo")
        return

    print("Apagado com sucesso" if achou else "Não achei esse WOD")

def filtrar():
    print("\n--- Filtrar WODs ---")
    print("1) Por tipo")
    print("2) Por movimento")
    esc = input("Selecione uma opção: ")

    try:
        with open("wods.txt", "r") as f:
            dados = f.readlines()
    except:
        print("Falha na tentativa de abrir o arquivo")
        return

    if not dados:
        print("Nenhum WOD cadastrado")
        return

    filtro = input("Digite o que deseja buscar: ").upper()
    encontrou_algum = False

    for linha in dados:
        linha = linha.strip()
        campos = linha.split(";")
        if len(campos) < 5:
            continue

        tipo = campos[1].upper()
        movimentos = campos[4].upper()

        if (esc == "1" and filtro in tipo) or (esc == "2" and filtro in movimentos):
            print("\nData:", campos[0])
            print("Tipo:", campos[1])
            print("Séries:", campos[2])
            print("Repetições:", campos[3])
            print("Movimentos:", campos[4])
            print("------------------")
            encontrou_algum = True

    if not encontrou_algum:
        print("Nenhum resultado foi encontrado com esse filtro.")
def checar_arquivo_metas():
    if not os.path.exists("metas.txt"):
        with open("metas.txt", "w"):
            pass  # só cria o arquivo vazio
def add_meta():
    checar_arquivo_metas()
    print("\n--- Nova Meta ---")
    d = input("Data (meta): ")
    objetivo = input("Objetivo: ")
    prazo = input("Prazo: ")
    progresso = input("Progresso atual (0-100%): ")

    try:
        progresso = int(progresso)
        if progresso >= 100:
            print("Meta já está concluída e não será salva.")
            return
    except ValueError:
        print("Progresso deve ser um número.")
        return

    try:
        with open("metas.txt", "a") as f:
            f.write(f"{d};{objetivo};{prazo};{progresso}\n")
        print("Meta salva!\n")
    except:
        print("Erro ao salvar a meta")

def ver_metas():
    checar_arquivo_metas()
    print("\n-- METAS --")
    try:
        with open("metas.txt") as f:
            linhas = f.readlines()
    except:
        print("Erro abrindo o arquivo de metas")
        return

    if not linhas:
        print("Nenhuma meta cadastrada")
        return

    for l in linhas:
        partes = l.strip().split(";")
        if len(partes) < 4:
            continue
        print(f"Data: {partes[0]}")
        print(f"Objetivo: {partes[1]}")
        print(f"Prazo: {partes[2]}")
        print(f"Progresso: {partes[3]}%")
        print("------------------")

def edit_meta():
    checar_arquivo_metas()
    print("\n--- Editar Meta ---")
    try:
        with open("metas.txt", "r") as f:
            todas = f.readlines()
    except:
        print("Erro ao abrir o arquivo")
        return

    if not todas:
        print("Nenhuma meta para editar")
        return

    ver_metas()
    data_alvo = input("Data da meta que quer editar: ")
    novo = ""
    achei = False

    for l in todas:
        c = l.strip().split(";")
        if c[0] == data_alvo:
            achei = True
            print("1) Objetivo\n2) Prazo\n3) Progresso")
            escolha = input("Qual campo deseja editar: ")

            if escolha == "1":
                c[1] = input("Novo objetivo: ")
            elif escolha == "2":
                c[2] = input("Novo prazo: ")
            elif escolha == "3":
                try:
                    novo_prog = int(input("Novo progresso (0-100%): "))
                    if novo_prog >= 100:
                        print("Meta concluída! Ela será removida.")
                        continue  # não inclui no novo arquivo
                    c[3] = str(novo_prog)
                except ValueError:
                    print("Progresso inválido.")
                    return
            else:
                print("Opção inválida")
                return

            nova_linha = ";".join(c) + "\n"
            novo += nova_linha
        else:
            novo += l

    try:
        with open("metas.txt", "w") as f:
            f.write(novo)
        print("Meta editada com sucesso")
    except:
        print("Erro ao salvar a meta editada")

    if not achei:
        print("Nenhuma meta encontrada com essa data")
import random

def sugerir_wod():
    print("\n--- Sugestão Aleatória de WOD ---")
    try:
        f = open("wods.txt", "r")
        linhas = f.readlines()
        f.close()
    except:
        print("Erro ao abrir o arquivo")
        return

    if not linhas:
        print("Nenhum WOD cadastrado ainda.")
        return

    escolhido = random.choice(linhas).strip().split(";")
    print("Aqui vai um WOD aleatório pra você tentar repetir ou se inspirar:\n")
    print("Data:", escolhido[0])
    print("Tipo:", escolhido[1])
    print("Séries:", escolhido[2])
    print("Repetições:", escolhido[3])
    print("Movimentos:", escolhido[4])

def conquistas():
    print("\n--- Conquistas ---")
    try:
        f = open("wods.txt", "r")
        linhas = f.readlines()
        f.close()
    except:
        print("Erro ao acessar os WODs")
        return

    if not linhas:
        print("Nenhum WOD cadastrado ainda.")
        return

    total_wods = len(linhas)
    tipos = set()
    movimentos = []
    contagem_movimentos = {}

    for l in linhas:
        c = l.strip().split(";")
        tipos.add(c[1].strip().upper())
        for m in c[4].split(","):
            mov = m.strip().upper()
            movimentos.append(mov)
            if mov in contagem_movimentos:
                contagem_movimentos[mov] += 1
            else:
                contagem_movimentos[mov] = 1

    print(f"\nVocê já cadastrou {total_wods} WOD(s)")

    if total_wods >= 1:
        print("✅ Primeiro treino registrado!")
    if total_wods >= 10:
        print("🏅 Medalha de Consistência: 10 ou mais WODs registrados!")
    if total_wods >= 20:
        print("🏅🏅 Medalha de Foco: 20 ou mais WODs registrados!")

    if len(tipos) >= 3:
        print("🧠 Usou todos os tipos de treino! (AMRAP, EMOM e FOR TIME)")
    elif len(tipos) >= 2:
        print("🤸‍♂ Medalha de Versatilidade: 2 ou mais tipos diferentes!")

    if len(set(movimentos)) >= 10:
        print("🤸‍♀🤸‍♀ Medalha de Diversidade: 10 ou mais movimentos diferentes usados!")

    favorito = max(contagem_movimentos, key=contagem_movimentos.get)
    qtd = contagem_movimentos[favorito]
    if qtd >= 5:
        print(f"⭐ Movimento favorito: {favorito} apareceu {qtd} vezes!")

    print("\nContinue se desafiando para conquistar mais medalhas 💪")
menu()
