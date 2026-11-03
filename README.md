# CasaStock 🏠

**Controle inteligente de estoque doméstico** — projeto acadêmico desenvolvido para a ExpoTech.

O CasaStock ajuda a acompanhar alimentos, bebidas, produtos de limpeza e itens de higiene da casa. O painel mostra o que existe no estoque, o que está acabando e o que está em falta.

## Funcionalidades
- Painel com resumo de produtos e quantidades.
- Cadastro, edição e exclusão de produtos.
- Aumento e redução rápida de quantidades.
- Categorias: alimentos, bebidas, limpeza, higiene e outros.
- Alertas de estoque baixo e produtos em falta.
- Pesquisa e filtros por categoria e situação.
- Exportação dos produtos filtrados para CSV.
- Persistência local com SQLite.
- Interface adaptável a computadores e celulares.
- Dados de demonstração na primeira execução.

## Tecnologias
Python, Flask, SQLite, HTML5, CSS3 e JavaScript.

## Como executar

Requisitos: Python 3.10 ou superior.

### Atalho para Windows (mais fácil)

1. Baixe o projeto pelo botão **Code > Download ZIP** no GitHub e extraia a pasta.
2. Certifique-se de que o Python 3.10 ou superior está instalado.
3. Abra a pasta extraída e dê dois cliques em **INICIAR_CASASTOCK.bat**.
4. Na primeira execução, o atalho cria o ambiente virtual e instala o Flask automaticamente.
5. O navegador abrirá o sistema em http://127.0.0.1:5000. Mantenha aberta a janela **CasaStock - Servidor** enquanto estiver usando o sistema.

Para encerrar, pressione **Ctrl+C** na janela do servidor ou feche essa janela.


```bash
git clone https://github.com/miguelaviladealmeida1-eng/casastock.git
cd casastock
python -m venv .venv
```

Ative o ambiente virtual:

**Windows (Prompt de Comando):**
```bat
.venv\Scripts\activate
```

**Linux:**
```bash
source .venv/bin/activate
```

Instale as dependências e inicie:
```bash
python -m pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000 no navegador.

## Estrutura
- `app.py`: servidor Flask e API.
- `templates/index.html`: interface.
- `static/style.css`: estilos.
- `static/app.js`: interações da interface.
- `requirements.txt`: dependências Python.
- `casastock.db`: banco SQLite criado automaticamente (não versionado).

## Uso em máquina virtual
O projeto pode ser executado em uma VM Linux ou Windows com Python instalado. Para acessar de outro dispositivo na mesma rede, use o IP da VM na porta 5000 e permita a porta no firewall. Para uma demonstração isolada, acessar pelo navegador da própria VM é suficiente.

## Observação
Os dados ficam no arquivo local `casastock.db`. Faça cópias de segurança desse arquivo se quiser preservar os cadastros.

Desenvolvido para fins acadêmicos — ExpoTech.
