from datetime import datetime

while True:
    data_vencimento = input('Informe a data de vencimento: (dd/mm/aaaa)\n')
    try:
        data_vencimento_corrigida = datetime.strptime(data_vencimento, '%d/%m/%Y').date()
        break
    except ValueError:
        print('Formato inválido. Tente uma data válida.\n')

while True:
    try:
        valor = float(input('Informe o valor: \n'))
        break
    except ValueError:
        print('Digite um valor válido.\n')

data_atual = datetime.today().date()
multa = 0.025
dias = (data_atual - data_vencimento_corrigida).days

if dias > 0:
    juros = dias * multa * dias
    total = valor + juros
else:
    juros = 0
    total = valor

print(f'\nDias de atraso: {dias}')
print(f'Juros: R$ {juros:.2f}')
print(f'Valor total a pagar: R$ {total:.2f}')