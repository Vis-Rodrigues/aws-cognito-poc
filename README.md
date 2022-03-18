# aws-cognito-poc
[![Generic badge](https://img.shields.io/badge/Linguagem-Python-yellow.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/pt/lambda/)

Projeto Prova de Conceito (POC) das funcionalidades do AWS Cognito.

## Lambda Layer
O Lambda Layer é uma feature da AWS para armazenar as libs dos lambdas, fazendo com que os pacotes tenham um tamanho reduzido.

Este projeto utiliza o lambda-layer com a lib do JWT. Siga os passos abaixo para atualizar o layer **hmv-layer** utilizado por este projeto:

1. Atualizar as libs no arquivo requirements.txt
2. Instalar as dependências:
> pip install -r requirements.txt -t python
3. Compactar a pasta de python com o nome **layer.zip**
> zip -r layer.zip python
4. Criar uma nova versão do layer e fazer o upload do **layer.zip**

### :exclamation: Atualizar o código no lambda
Execute o comando abaixo para gerar o **hmv-signup.zip** e depois faça o upload no lambda pelo console da AWS
> zip -r poc-cognito.zip * -x ".git*" -x "*.zip" -x "README.md" -x coverage.xml -x "venv/*" -x ./package -x "tests/*" -x "test/*" -x 'python/*' -x Dockerfile -x docker-compose.yml

