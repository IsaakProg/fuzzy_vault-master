**CODIGO ATUALIZADO** (2014-2023)

Implementação de um sistema de autentição simples usando o algoritom do fuzzy vault 
[**A Fuzzy Vault Scheme**](http://people.csail.mit.edu/madhu/papers/2002/ari-journ.pdf). 
[**Deep Face Fuzzy Vault: Implementation and Performance**](https://paperswithcode.com/paper
deep-face-fuzzy-vault-implementation-and)



1. Os dados "biométricos" são representados como uma lista de dez números decimais (FLOATS). (O AUTOR DESCREVE QUE DADOS DE DIGITAIS REAIS SÃO MAIS COMPLEXOS)

2. Eu simplifiquei a interpolação polinomial - em vez de usar códigos [Reed-Solomon](http://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction), eu usei uma função de ajuste polinomial.

3. Pontos "Chaff" não são descartados se colidirem com pontos genuínos no polinômio.

Para executar o programa, escolha um arquivo de impressão digital do diretório `fingerprints`, por exemplo, `ming`, e execute:

```python3 authenticate.py fingerprints/ming```

Este programa importa uma lista de vaults, que foram criados usando "impressões digitais" (modelos biométricos). Cada cofre armazena dados de impressão digital criptografados vinculados a uma chave secreta (ou seja, o nome da pessoa). Portanto, quando `authenticate.py` é rodado com o modelo fornecido, tentamos desbloquear cada vault para obter o nome criptografado nele. Se o modelo for uma correspondência próxima o suficiente com o modelo original usado para criar o cofre e o nome retornado estiver em uma lista de usuários conhecidos, obtemos uma correspondência e o usuário é aceito.
