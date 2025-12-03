import json

with open('vendas_desafio1.json', 'r', encoding='utf-8') as arquivo:
    vendas = json.load(arquivo)

vendedores = {}

for venda in vendas['vendas']:
    vendedor = venda['vendedor']
    if vendedor not in vendedores:
        vendedores[vendedor] = []
    vendedores[vendedor].append(venda['valor'])

for vendedor, valor in vendedores.items():
    frase = f'{vendedor} fez:'
    print(frase)
    v1 = v2 = v3 = 0
    c1 = c2 = c3 = t = 0
    for v in valor:
        if v < 100:
            v1 += 1
            c1 += v
        elif v < 500:
            v2 += 1
            c2 += v * 1.01
        else:
            v3 += 1
            c3 += v * 1.05
    t = c1 + c2 + c3
    print(f'{' ' * len(frase)}{v1} venda(s) abaixo de R$100, somando R${c1:.2f}\n'
          f'{' ' * len(frase)}{v2} venda(s) entre R$100 e R$500, somando R${c2:.2f}\n'
          f'{' ' * len(frase)}{v3} e venda(s) acima de R$500, somando R${c3:.2f}\n'
          f'{' ' * len(frase)}Total de vendas foi de R${t:.2f}.\n')
