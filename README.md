# Sistema de Controle de Chamados de TI

Sistema desktop desenvolvido em **Python** para gerenciamento de chamados de suporte técnico, permitindo registrar, consultar, acompanhar, atualizar e encerrar solicitações de usuários.

O projeto foi desenvolvido como parte do meu portfólio profissional com foco na aplicação prática de conhecimentos em **Python, SQL, banco de dados, desenvolvimento de sistemas, interface gráfica e geração de relatórios**.

---

## Sobre o projeto

O sistema simula o funcionamento de uma ferramenta interna de atendimento de TI, onde usuários podem registrar problemas ou solicitações e a equipe de suporte pode acompanhar o andamento dos chamados.

A aplicação permite controlar todo o ciclo de atendimento:

**Abertura → Atendimento → Solução → Encerramento**

Além do gerenciamento dos chamados, o sistema disponibiliza indicadores e relatórios para facilitar o acompanhamento das solicitações.

---

## Objetivos

O projeto foi desenvolvido com os seguintes objetivos:

* Praticar desenvolvimento de aplicações desktop com Python.
* Trabalhar com banco de dados relacional.
* Aplicar comandos SQL para inclusão, consulta e atualização de dados.
* Desenvolver uma interface gráfica funcional.
* Implementar filtros e consultas de informações.
* Criar indicadores para acompanhamento dos chamados.
* Gerar relatórios para análise dos dados.
* Integrar a aplicação com arquivos Excel.
* Aplicar organização modular de código.
* Desenvolver um projeto completo para portfólio profissional.

---

## Funcionalidades

### Cadastro de chamados

Permite registrar:

* Solicitante
* Setor
* Categoria
* Descrição do problema
* Prioridade
* Responsável pelo atendimento
* Data de abertura

O sistema gera automaticamente um número de identificação para cada chamado.

### Controle de status

Cada chamado pode possuir um dos seguintes status:

* **Aberto**
* **Em atendimento**
* **Encerrado**

Quando um chamado é encerrado, o sistema registra a solução aplicada e a data de encerramento.

### Consulta de chamados

A aplicação permite consultar os chamados cadastrados e utilizar filtros para facilitar a localização das informações.

Filtros disponíveis:

* Status
* Prioridade
* Categoria

Também é possível atualizar a listagem após novos registros ou alterações.

### Gerenciamento de chamados

Através da tela de gerenciamento é possível:

* Localizar um chamado pelo ID.
* Visualizar os dados do atendimento.
* Alterar o status.
* Registrar ou atualizar a solução.
* Encerrar o chamado.
* Atualizar automaticamente os indicadores do sistema.

### Indicadores

A tela principal apresenta indicadores gerais do atendimento:

* Total de chamados
* Chamados abertos
* Chamados em atendimento
* Chamados encerrados

Esses indicadores permitem visualizar rapidamente a situação atual dos chamados.

### Relatórios

O sistema apresenta informações agrupadas por:

* Status
* Prioridade
* Categoria

Também é possível exportar os chamados cadastrados para uma planilha Excel.

---

## Relatório em Excel

A aplicação gera automaticamente o arquivo:

```text
relatorios/relatorio_chamados.xlsx
