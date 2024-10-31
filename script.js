// Dicionário para armazenar o estoque
const estoque = {};

// Função para adicionar um produto
function adicionarProduto() {
    const nome = document.getElementById('nome').value;
    const quantidade = parseInt(document.getElementById('quantidade').value);
    const tipo = document.getElementById('tipo').value;

    if (!nome || isNaN(quantidade) || !tipo) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    if (estoque[nome]) {
        estoque[nome].quantidade += quantidade;
        alert(`Produto '${nome}' atualizado com mais ${quantidade} unidades.`);
    } else {
        estoque[nome] = { quantidade, tipo };
        alert(`Produto '${nome}' adicionado com ${quantidade} unidades.`);
    }

    atualizarTabela();
    limparCampos();
}

// Função para retirar um produto
function retirarProduto() {
    const nome = document.getElementById('retirarNome').value;
    const quantidade = parseInt(document.getElementById('retirarQuantidade').value);

    if (!nome || isNaN(quantidade)) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    if (estoque[nome]) {
        if (estoque[nome].quantidade >= quantidade) {
            estoque[nome].quantidade -= quantidade;
            alert(`${quantidade} unidades de '${nome}' foram retiradas do estoque.`);
            if (estoque[nome].quantidade === 0) {
                delete estoque[nome];
                alert(`O produto '${nome}' está agora esgotado e foi removido do estoque.`);
            }
        } else {
            alert(`Estoque insuficiente para '${nome}'. Quantidade disponível: ${estoque[nome].quantidade}.`);
        }
    } else {
        alert(`O produto '${nome}' não está no estoque.`);
    }

    atualizarTabela();
    limparCampos();
}

// Função para atualizar a tabela de produtos
function atualizarTabela() {
    const tabela = document.getElementById('estoqueTabela');
    tabela.innerHTML = '';

    for (const [nome, info] of Object.entries(estoque)) {
        const linha = document.createElement('tr');
        linha.innerHTML = `<td>${nome}</td><td>${info.quantidade}</td><td>${info.tipo}</td>`;
        tabela.appendChild(linha);
    }
}

// Função para limpar os campos de entrada
function limparCampos() {
    document.getElementById('nome').value = '';
    document.getElementById('quantidade').value = '';
    document.getElementById('tipo').value = '';
    document.getElementById('retirarNome').value = '';
    document.getElementById('retirarQuantidade').value = '';
}
