# Sistema de Controle de Chamados de TI

Sistema desenvolvido em Python para gerenciamento de chamados de suporte técnico, utilizando SQLite como banco de dados e Tkinter para construção da interface gráfica.

O projeto simula uma aplicação de Help Desk, permitindo registrar, consultar, acompanhar, atualizar e encerrar chamados de TI.

---

## 🎯 Objetivo

Desenvolver uma aplicação simples e funcional para gerenciamento de chamados de suporte técnico, aplicando conceitos de:

- Desenvolvimento em Python
- Banco de dados SQLite
- SQL
- Interface gráfica com Tkinter
- CRUD
- Filtros e consultas
- Indicadores
- Exportação de relatórios
- Organização de projeto
- Versionamento com Git e GitHub

---

## ⚙️ Funcionalidades

### Cadastro de chamados

Permite registrar novos chamados informando:

- Solicitante
- Setor
- Categoria
- Descrição
- Prioridade
- Responsável

O sistema registra automaticamente a data e o número do chamado.

### Consulta de chamados

Permite consultar os chamados cadastrados e utilizar filtros por:

- Status
- Prioridade
- Categoria

Também apresenta as principais informações dos chamados em uma tabela.

### Gerenciamento de chamados

Permite localizar um chamado pelo número e atualizar:

- Status
- Solução
- Data de encerramento

Os status disponíveis são:

- Aberto
- Em atendimento
- Encerrado

### Indicadores

A tela principal apresenta:

- Total de chamados
- Chamados abertos
- Chamados em atendimento
- Chamados encerrados

### Relatórios

O sistema apresenta consultas agrupadas por:

- Status
- Prioridade
- Categoria

Também permite exportar os dados dos chamados para uma planilha Excel.

---

## 📊 Relatório Excel

O sistema gera automaticamente o arquivo:

`relatorio_chamados.xlsx`

O relatório contém:

- ID do chamado
- Data de abertura
- Solicitante
- Setor
- Categoria
- Descrição
- Prioridade
- Responsável
- Status
- Solução
- Data de encerramento

---

## 🛠️ Tecnologias utilizadas

- Python
- SQLite
- SQL
- Tkinter
- OpenPyXL
- Git
- GitHub

---

## 🗄️ Banco de dados

O sistema utiliza o SQLite, um banco de dados relacional que não necessita de instalação ou configuração de servidor.

A tabela principal utilizada pelo sistema é:

### `chamados`

Principais campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único do chamado |
| `data_abertura` | Data e hora de abertura |
| `solicitante` | Nome do solicitante |
| `setor` | Setor do solicitante |
| `categoria` | Categoria do chamado |
| `descricao` | Descrição do problema |
| `prioridade` | Prioridade do atendimento |
| `responsavel` | Responsável pelo atendimento |
| `status` | Situação atual do chamado |
| `solucao` | Solução aplicada |
| `data_encerramento` | Data e hora do encerramento |

---

## 📁 Estrutura do Projeto

```text
Controle_Chamados_TI/
│
├── banco/
│   └── chamados.db
│
├── src/
│   ├── banco.py
│   ├── chamados.py
│   ├── relatorios.py
│   └── main.py
│
├── imagens/
│   ├── menu-principal.png
│   ├── novo-chamado.png
│   ├── consulta-chamados.png
│   ├── gerenciar-chamado.png
│   ├── relatorios.png
│   └── relatorio-excel.png
│
├── relatorios/
│   └── relatorio_chamados.xlsx
│
├── .gitignore
└── README.md
