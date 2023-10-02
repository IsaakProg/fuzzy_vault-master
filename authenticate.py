#Este é o arquivo principal de autenticação. 
#Ele recebe como entrada um arquivo contendo uma "impressão digital"
#ou um template biométrico e tenta desbloquear um vault usando esse template.
#Se for bem-sucedido, ele identifica o usuário e printa uma saudação com o nome desse usuário. 
#Caso contrário, ele informa que o usuário é desconhecido.


# Importações de módulos
from vaults import vaults              # Importa os cofres (vaults) a partir de vaults.py
from fuzzy_vault import unlock, decode  # Importa funções de desbloqueio e decodificação
from sys import argv                   # Importa argv para acessar argumentos de linha de comando
import warnings                        # Importa o módulo de avisos

# Lista de nomes conhecidos
known = ['jayme woogerd', 'norman ramsey', 'ming chow']

# Suprimir mensagens de aviso durante a execução
warnings.filterwarnings("ignore")

def main():
    # Verifique se o usuário forneceu um argumento de linha de comando
    if len(argv) != 2:
        print("Usage: python authenticate.py fingerprints/jayme")
        return

    # Abrir e ler o arquivo de template biométrico especificado pelo usuário
    with open(argv[1], 'r') as f:
        template = f.readlines()
        template = [float(t) for t in template]

    # Iterar sobre os cofres (vaults) disponíveis
    for vault in vaults:
        # Tente desbloquear o cofre com o template biométrico
        coeffs = unlock(template, vault)
        try:
            # Tente decodificar os coeficientes e verificar se o nome está na lista de conhecidos
            name = decode(coeffs)
            if name in known:
                print('Hello, %s!' % name.title())  # PRINT uma saudação se o usuário for reconhecido
                return
        except TypeError:
            pass

    # Se o usuário não for reconhecido, PRINT "Unknown user"
    print("Unknown user")

if __name__ == '__main__':
    # Chama a função principal se o script for executado diretamente
    main()
