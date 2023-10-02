#Este arquivo implementa as funções principais para criar e manipular o fuzzy vault. 
#Ele inclui funções como lock para criar um cofre, unlock para tentar desbloquear um cofre com base em um
#template biométrico e decode para decodificar os coeficientes de um cofre desbloqueado de volta a uma palavra secreta.

#Este arquivo implementa o algoritmo do fuzzy vault e pode ser usado para criar cofres,
#que criptografam uma chave secreta com dados biométricos.
#O cofre pode ser desbloqueado se for apresentado um modelo suficientemente semelhante.

# Importações de módulos
from random import uniform, shuffle  # Importa funções relacionadas à geração de números aleatórios
from numpy import polyfit           # Importa polyfit do módulo numpy
import real                          # Importa um módulo chamado real (provavelmente contendo dados biométricos)

degree = 4  # Grau do polinômio
t = 10      # Número de características em cada template
r = 40      # Número de pontos falsos (chaff points)

def get_coefficients(word):
    # Codifica uma palavra secreta como coeficientes de um polinômio
    # Retorna uma lista de coeficientes
    word = word.upper()
    n = len(word) // degree
    if n < 1:
        n = 1
    substrings = [word[i:i + n] for i in range(0, len(word), n)] 
    coeffs = []
    for substr in substrings:
        num = 0
        for x, char in enumerate(substr):
            num += ord(char) * 100**x
        coeffs.append(num**(1/3.0))
    return coeffs

def p_x(x, coeffs):
    # Retorna o valor de p(x) para o x dado, onde p(x) é um polinômio definido por seus coeficientes
    y = 0
    degree = len(coeffs) - 1

    for coeff in coeffs:
        y += x**degree * coeff
        degree -= 1

    return y

def lock(secret, template):
    # Dado um segredo para codificar e um template biométrico, cria e retorna um vault fuzzy onde os dados são criptografados
    vault = []
    coeffs = get_coefficients(secret)

    # Calcula os pontos genuínos
    for point in template:
        vault.append([point, p_x(point, coeffs)])

    # Adiciona pontos falsos (chaff points)
    max_x = max(template)
    max_y = max([y for [x, y] in vault])

    for i in range(t, r):
        x_i = uniform(0, max_x * 1.1)
        y_i = uniform(0, max_y * 1.1)
        vault.append([x_i, y_i])
    shuffle(vault)
    return vault

def approx_equal(a, b, epsilon):
    # Verifica se dois números são aproximadamente iguais com base em uma margem de erro (epsilon)
    return abs(a - b) < epsilon

def unlock(template, vault):
    # Dado um template biométrico e um fuzzy vault, retorna os coeficientes usados para codificar o segredo ou None se o template não corresponder
    def project(x):
        for point in vault:
            if approx_equal(x, point[0], 0.001):
                return [x, point[1]]
        return None

    Q = list(zip(*[project(point) for point in template if project(point) is not None]))
    try:
        return polyfit(Q[0], Q[1], deg=degree)
    except IndexError:
        return None

def decode(coeffs):
    # Dado um conjunto de coeficientes, decodifica a palavra secreta
    s = ""
    for c in coeffs:
        num = int(round(c**3))
        if num == 0:
            continue
        while num > 0:
            s += str(chr(num % 100)).lower()
            num //= 100
    return s

def main():
    # Escreve os cofres (vaults) gerados a partir dos dados biométricos no arquivo 'vaults.py'
    with open('vaults.py', 'w+') as f:
        f.write('vaults = [')
        for p in real.people: 
            f.write(str(lock(p, real.people[p])))
            f.write(',')
        f.write(']')

if __name__ == '__main__':
    # Chama a função principal se o script for executado diretamente
    main()
