from time import sleep, strftime
import json

def lerJson(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f'Erro ao ler {nome_arquivo}: {e}.')
        return []

def salvarJson(dados, nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Erro ao salvar {nome_arquivo}: {e}.')

dados_estoque_json = lerJson('estoque_desafio2.json')
estoque = dados_estoque_json.get('estoque', [])
movimentacoes = lerJson('movimentacoes.json')
data_atual = strftime('%d/%m/%Y %H:%M:%S')
codigoProduto = None

def salvarEstoque(estoque):
    salvarJson({'estoque': estoque}, 'estoque_desafio2.json')

def salvarMovimentacoes(movimentacoes):
    salvarJson(movimentacoes, 'movimentacoes.json')



def adicionar_produto_novo(estoque, movimentacoes, data_atual):
    produtoNovo = input('Produto: ').strip().lower()
    if not produtoNovo.isalpha():
        print('✖ Valor inválido! Digite apenas letras.')

    for p in estoque:
        if p['descricaoProduto'].strip().lower() == produtoNovo:
            print('✖ Produto já consta no estoque.')
            return

    quantidade = int(input('Quantidade: ').strip())
    novoCodigo = max([p['codigoProduto'] for p in estoque]) + 1
    produtoNovo = {'codigoProduto': novoCodigo,
               'descricaoProduto': produtoNovo.title(),
               'estoque': quantidade}
    estoque.append(produtoNovo)

    movimentacoes.append({
        'tipo': 'Produto Novo',
        'descricaoProduto': produtoNovo,
        'estoque': quantidade,
        'data': data_atual
    })
    ultimaMovimentacao = movimentacoes[-1]
    salvarEstoque(estoque)
    salvarMovimentacoes(movimentacoes)
    print(f'Produto adicionado com sucesso!')
    for chave, valor in ultimaMovimentacao.items():
        print(f"{chave:<12}: {valor}")
    return estoque

def remover_produto(estoque):
    print('Digite o código ou nome do produto para remove-lo.')
    remover = input('Produto a ser removido: ').strip().lower()
    if remover.isalpha() or remover.isdigit():
        pass
    else:
        print('✖ Entrada inválida! Digite apenas letras ou apenas números.')
        return

    index = None
    for i, r in enumerate(estoque):
        nome = r['descricaoProduto'].strip().lower()
        codigo = r['codigoProduto']
        if nome == remover or str(codigo) == remover:
            index = i
            break
    if index is not None:
        produto = estoque.pop(index)
        movimentacoes.append({
             'tipo': 'Produto Removido',
             'descricaoProduto': produto['descricaoProduto'],
             'codigoProduto': produto['codigoProduto'],
             'data': data_atual
                })
        salvarEstoque(estoque)
        salvarMovimentacoes(movimentacoes)
        print(f'Produto removido com sucesso!')
        ultimamovimentacao = movimentacoes[-1]
        for chave, valor in ultimamovimentacao.items():
            print(f"{chave:<12}: {valor}")
    else:
        print('Opção inválida!')

    return estoque

def entrada_produto(estoque, movimentacoes, data_atual):
    produtoExistente = input('Produto para incrementar: ').strip().lower()
    if produtoExistente.isalpha():
        pass
    else:
        print('✖ Entrada inválida! Digite apenas letras.')
        return

    index = None
    for i, p in enumerate(estoque):
        nome = p['descricaoProduto'].lower()

        if produtoExistente == nome:
            index = i
            break
    if index is None:
        print('Produto não encontrado!')
        return estoque

    produto = estoque[index]

    try:
        quantidade = int(input('Quantidade: ').strip())
    except ValueError:
        print('Quantidade deve ser em números inteiros.')
        return estoque

    if quantidade < 0:
        print('Quantidade deve ser maior que zero.')
        return estoque

    produto['estoque'] += quantidade

    movimentacoes.append({
        'tipo': 'Incremento de Estoque',
        'descricaoProduto': produto['descricaoProduto'],
        'codigoProduto': produto['codigoProduto'],
        'estoque': quantidade,
        'data': data_atual
    })
    salvarEstoque(estoque)
    salvarMovimentacoes(movimentacoes)
    print(f'Incremento de {quantidade} unidades de {produto['descricaoProduto']}.'
          f' Estoque atual: {produto['estoque']}')
    ultimamovimentacao = movimentacoes[-1]
    for chave, valor in ultimamovimentacao.items():
        print(f"{chave:<12}: {valor}")
    return estoque

def saida_produto(estoque, movimentacoes, data_atual):
    produtoExistente = input('Produto para decrementar: ').strip().lower()
    if produtoExistente.isalpha():
        pass
    else:
        print('✖ Entrada inválida! Digite apenas letras.')
        return

    index = None
    for i, p in enumerate(estoque):
        nome = p['descricaoProduto'].lower()

        if produtoExistente == nome:
            index = i
            break
    if index is None:
        print('Produto não encontrado!')
        return estoque

    produto = estoque[index]

    try:
        quantidade = int(input('Quantidade: ').strip())
    except ValueError:
        print('Quantidade deve ser em números inteiros.')
        return estoque

    if quantidade < 0:
        print('Quantidade deve ser maior que zero.')
        return estoque

    produto['estoque'] -= quantidade

    movimentacoes.append({
        'tipo': 'Decremento de Estoque',
        'descricaoProduto': produto['descricaoProduto'],
        'codigoProduto': produto['codigoProduto'],
        'estoque': quantidade,
        'data': data_atual
    })
    salvarEstoque(estoque)
    salvarMovimentacoes(movimentacoes)
    print(f'Decremento de {quantidade} unidades de {produto['descricaoProduto']}.'
          f' Estoque atual: {produto['estoque']}')
    ultimamovimentacao = movimentacoes[-1]
    for chave, valor in ultimamovimentacao.items():
        print(f"{chave:<12}: {valor}")
    return estoque

def verEstoque(estoque):
    if estoque:
        linha('=', 40)
        print('          ESTOQUE ATUAL          ')
        linha('=', 40)
        print(f"{'Código':<8} {'Produto':<20} {'Qtd':>6}")
        linha('-', 40)
        for p in estoque:
            print(f"{p['codigoProduto']:<8} {p['descricaoProduto']:<20} {p['estoque']:>6}")
        linha('=', 40)
    else:
        print('Estoque vazio.\n')
        return

def verMovimentacoes(movimentacoes):
    if movimentacoes:
        print('\n' + '=' * 60)
        print('          MOVIMENTAÇÕES          ')
        print('=' * 60)
        print(f"{'Data':<20} {'Tipo':<20} {'Produto':<20} {'Código':<6} {'Qtd':>5}")
        print('-' * 60)
        for m in movimentacoes:
            produto_nome = m['descricaoProduto']['descricaoProduto'] if isinstance(m['descricaoProduto'], dict) else m['descricaoProduto']
            codigo = m['descricaoProduto']['codigoProduto'] if isinstance(m['descricaoProduto'], dict) else m['codigoProduto']
            quantidade = m['estoque'] if 'estoque' in m else ''

            print(f"{m['data']:<20} {m['tipo']:<20} {produto_nome:<20} {codigo:<6} {quantidade:>5}")

        print('=' * 60 + '\n')
    else:
        print('Não houveram movimentações.\n')
        return

def linha(caractere = '-', tamanho = 30):
    print(caractere * tamanho)

AZUL = '\033[94m'
RESET = '\033[0m'

while True:
    linha('=', 30)
    print('-=-=-=-= MENU -=-=-=-=\n'
          'O QUE DESEJA FAZER?\n'
          f'{AZUL}[1]{RESET} - VER ESTOQUE ATUAL\n'
          f'{AZUL}[2]{RESET} - ADICIONAR UM PRODUTO NOVO\n'
          f'{AZUL}[3]{RESET} - REMOVER PRODUTO\n'
          f'{AZUL}[4]{RESET} - INCREMENTAR A QUANTIDADE DE UM PRODUTO\n'
          f'{AZUL}[5]{RESET} - DECREMENTAR A QUANTIDADE DE UM PRODUTO\n'
          f'{AZUL}[6]{RESET} - HISTÓRICO DE MOVIMENTAÇÕES\n'
          f'{AZUL}[7]{RESET} - SAIR')
    linha('=', 30)

    try:
        escolha = int(input('Qual a sua escolha: \n').strip())
    except ValueError:
        print('Valor inválido! Digite apenas números.')

    if escolha == 1:
        verEstoque(estoque)
    elif escolha == 2:
        adicionar_produto_novo(estoque, movimentacoes, data_atual)
    elif escolha == 3:
        remover_produto(estoque)
    elif escolha == 4:
        entrada_produto(estoque, movimentacoes, data_atual)
    elif escolha == 5:
        saida_produto(estoque, movimentacoes, data_atual)
    elif escolha == 6:
        verMovimentacoes(movimentacoes)
    elif escolha == 7:
        print('SAINDO DO PROGRAMA...')
        sleep(2)
        break
    else:
        print('Opção inválida!')

print('ATÉ A PRÓXIMA')