from delivery import Delivery
from dbConnector import Connector

def menu():
    print("""
Menu:
-------------
        1 - Consultar
        2 - Cadastrar
        3 - Deletar
        4 - Sair
    """)
    return int(input("Escolha uma opção: "))

def menu_keys(keys):
    if len(keys) == 0:
        print("\nNenhuma chave cadastrada!\n")
        return 0
    str_keys = "Chaves registradas: \n-------------\n\t0 - Voltar"

    for ind in range(len(keys)):
        str_keys += f"\n\t{ind + 1} - {keys[ind]}"
    
    print(str_keys)
    selecao = int(input("\nSelecione uma chave: "))
    
    try:
        if selecao == 0:
            return 0
        else:
            return keys[selecao - 1]
    except Exception:
        print("\nNão localizei esta chave, tente novamente!\n")
        return menu_keys(keys)


def main():
    db = Connector('danfes.db')

    while True:
        choice = menu()
        keys = []
        #Check
        if choice == 1:
            keys = db.retrieve_all_keys()
            key = menu_keys(keys)
            #If the selected key is higher than 0
            if key != 0:
                print(Delivery(key).get_events())
            else:
                continue
        #Register
        elif choice == 2:
            key = input("\nChave da DANFe: ")
            if len(key) >= 36:
                db.register(key)
            else:
                print("\nChave inválida!")
                continue
        #Delete
        elif choice == 3:
            keys = db.retrieve_all_keys()
            key = menu_keys(keys)
            #If the selected key is higher than 0
            if key != 0:
                db.delete(key)
            else:
                continue

if __name__ == "__main__":
    main()