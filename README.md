# 📇 Agenda de Contatos — Python

![Python](https://img.shields.io/badge/Python-3.14-blue) ![Status](https://img.shields.io/badge/Status-Em%20andamento-yellow)

Sistema de agenda de contatos via terminal, desenvolvido em Python com Programação Orientada a Objetos e persistência de dados em banco SQLite.

Projeto evoluído a partir de uma versão inicial simples (dicionário + arquivo `.txt`) até a arquitetura atual, modularizada em funções e com banco de dados relacional.

## 📋 Funcionalidades

- **Adicionar contato** — validação de duplicata e formato de telefone (11 dígitos)
- **Ver agenda completa** — listagem de todos os contatos cadastrados
- **Remover contato** — seleção por número na lista, com dupla confirmação antes de excluir
- **Buscar contato** — por nome completo ou por letra inicial
- **Editar contato** — alteração de nome com persistência imediata no banco
- **Ordenação alfabética** — reorganiza a agenda por ordem de nome
- **Sair** — encerra o programa e fecha a conexão com o banco

## 🛠️ Tecnologias e conceitos aplicados

- **Python 3.14**
- **POO (Programação Orientada a Objetos)** — classe `Contato` representando cada registro
- **SQLite** — persistência de dados via `sqlite3`, com queries parametrizadas (proteção contra SQL Injection)
- **Modularização** — cada operação do menu isolada em sua própria função
- **match/case** — controle de fluxo do menu principal
- **Git** — versionamento com histórico de commits organizado

## 🚀 Como executar

```bash
git clone https://github.com/rjsouzadev/contact-manager-python
cd contact-manager-python
python contact-manager-python.py
```

## 📈 Evolução do projeto

Este repositório documenta minha evolução prática com Python, migrando da lógica de programação (veja [logica-de-programacao]([link-aqui](https://github.com/rjsouzadev/logica-de-programacao))) para uma linguagem de mercado — passando por estruturas de dados simples, arquivos `.txt`, até chegar em banco de dados relacional e boas práticas de organização de código.

## 💡 Aprendizados

- Diferença entre tipos mutáveis e imutáveis em Python, e como isso afeta passagem de parâmetros em funções
- Uso de `return` para controlar fluxo de execução, eliminando flags booleanas desnecessárias
- Escopo de variáveis e organização de código em funções reutilizáveis
- Prevenção de SQL Injection com queries parametrizadas
- Fluxo básico de Git: `init`, `add`, `commit`, `remote`, `push`

## 🔜 Próximos passos

- Consumo de API para chatbot integrado
- Testes automatizados
- Interface gráfica ou web (avaliação futura)

## 👤 Autor

**Rogério Junior**
[LinkedIn](https://www.linkedin.com/in/rogerio-junior-422607365/) · [GitHub](https://github.com/rjsouzadev)
