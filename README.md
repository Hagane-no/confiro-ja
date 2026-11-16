# Confiro Já – Projeto Integrador II

## Descrição

O **Confiro Já** é uma aplicação web desenvolvida para auxiliar no gerenciamento e controle de estoque de unidades escolares. O sistema foi criado com o propósito de substituir os registros manuais realizados em cadernos por uma ferramenta informatizada, proporcionando maior organização, agilidade e confiabilidade no acompanhamento dos materiais disponíveis.

A plataforma permite registrar entradas e saídas de produtos, acompanhar o saldo atual do estoque, consultar o histórico de movimentações e analisar o consumo dos materiais. Além disso, possui um recurso de projeção que auxilia na identificação de tendências de consumo e na estimativa de quando determinado produto poderá acabar, contribuindo para o planejamento de futuras reposições.

## Objetivo

Desenvolver uma solução web prática e acessível para modernizar o controle de estoque escolar, reduzir falhas nos registros manuais, facilitar o acompanhamento dos materiais e fornecer informações que auxiliem na organização e no planejamento das compras e reposições.

## Participante

- Marcos Michel Amaral de Lima

## Tecnologias utilizadas

- **Python:** linguagem de programação principal.
- **Django:** framework utilizado no desenvolvimento da aplicação e no gerenciamento das funcionalidades.
- **HTML:** estruturação das páginas.
- **CSS:** estilização e apresentação visual.
- **SQLite:** banco de dados utilizado para armazenar as informações.
- **Git e GitHub:** controle de versão e armazenamento do código-fonte.
- **PythonAnywhere:** hospedagem da aplicação web.

## Funcionalidades

- **Gerenciamento de produtos:** cadastro, edição e controle da situação dos produtos.
- **Gerenciamento de categorias:** organização dos materiais por categorias.
- **Registro de movimentações:** lançamento de entradas e saídas de produtos.
- **Controle de saldo:** acompanhamento das quantidades disponíveis em estoque.
- **Histórico de movimentações:** consulta dos registros de entradas e saídas.
- **Dashboard:** painel inicial com informações gerais do estoque.
- **Projeção de estoque:** análise do consumo e estimativa de esgotamento dos produtos, auxiliando no planejamento de reposições.
- **Gerenciamento de usuários:** cadastro de funcionários e controle de acesso.
- **Aprovação de cadastros:** usuários administradores podem aprovar ou rejeitar solicitações de acesso de novos funcionários.
- **Controle administrativo:** gerenciamento das permissões e acompanhamento dos usuários cadastrados.

## Estrutura do projeto

- `config/` — configurações principais do projeto Django.
- `estoque/` — aplicação responsável pelo gerenciamento de produtos, categorias e movimentações.
- `usuarios/` — aplicação responsável pelo cadastro, autenticação e gerenciamento dos usuários.
- `templates/` — arquivos HTML utilizados na interface do sistema.
- `manage.py` — ferramenta de gerenciamento do projeto Django.
- `requirements.txt` — dependências necessárias para executar a aplicação.
- `.gitignore` — arquivos e diretórios que não devem ser enviados ao GitHub.
- `README.md` — documentação do projeto.

## Como executar o projeto localmente

**1. Clonar o repositório:**

```bash
git clone https://github.com/Hagane-no/confiro-ja.git
```

**2. Acessar a pasta do projeto:**

```bash
cd confiro-ja
```

**3. Criar um ambiente virtual:**

```bash
python -m venv venv
```

**4. Ativar o ambiente virtual:**

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

**5. Instalar as dependências:**

```bash
pip install -r requirements.txt
```

**6. Executar as migrações do banco de dados:**

```bash
python manage.py migrate
```

**7. Criar um usuário administrador:**

```bash
python manage.py createsuperuser
```

**8. Iniciar o servidor local:**

```bash
python manage.py runserver
```

Após iniciar o servidor, acessar:

http://127.0.0.1:8000/

## Acesso à aplicação

O sistema está hospedado no PythonAnywhere e pode ser acessado pelo endereço:

https://chibysan.pythonanywhere.com/

## Status do projeto

**Desenvolvido e disponível para acesso online.**

Projeto acadêmico desenvolvido como parte do Projeto Integrador II da UNIVESP.
