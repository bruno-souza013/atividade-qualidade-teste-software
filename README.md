# Tarefa 2.1 — Qualidade e Testes de Software

Este repositório reúne as atividades das aulas 15-20 e contém a implementação de uma API Flask, testes automatizados e pipelines CI conforme solicitado na atividade.

**Aulas incluídas**
- Aula 15 — API com Flask + Qualidade de Software
- Aula 16 — API com Flask + Qualidade de Software Pt.2
- Aula 17 — Tipos de Testes
- Aula 18 — Testes Funcionais
- Aula 19 — Testes End-To-End (E2E)
- Aula 20 — TDD (Test Driven Development)

**Requisitos da entrega**
- Testes automatizados: unitários, integração, funcionais e E2E (Selenium)
- Testes adicionais implementados: 10 unitários, 5 integração, 3 funcionais, 2 E2E
- Funcionalidade nova implementada via TDD (RED → GREEN → REFACTOR)
- CI configurado (GitHub Actions) executando `pytest`, `flake8` e `black --check` para as pastas relevantes

**Onde estão os arquivos importantes**
- Código e rotas: [aula-20/app/routes/user_routes.py](aula-20/app/routes/user_routes.py)
- Lógica de serviço (busca implementada): [aula-20/app/services/user_services.py](aula-20/app/services/user_services.py)
- Testes unitários (search): [aula-20/tests/unit/test_user_search.py](aula-20/tests/unit/test_user_search.py)
- Testes de integração: [aula-20/tests/integration/test_user_search_route.py](aula-20/tests/integration/test_user_search_route.py), [aula-20/tests/integration/test_user_routes_more.py](aula-20/tests/integration/test_user_routes_more.py)
- Testes funcionais: [aula-20/tests/functional/test_user_functional_2.py](aula-20/tests/functional/test_user_functional_2.py)
- Testes E2E (Selenium): [aula-20/tests/e2e/test_user_e2e_aula20.py](aula-20/tests/e2e/test_user_e2e_aula20.py) and [aula-20/tests/e2e/test_user_functional.py](aula-20/tests/e2e/test_user_functional.py)
- Workflows CI: [.github/workflows/ci-aula-16.yml](.github/workflows/ci-aula-16.yml) and [.github/workflows/ci-aula-20.yml](.github/workflows/ci-aula-20.yml)

Instalação e execução
----------------------
Recomendo criar um ambiente virtual e instalar dependências por aula quando necessário.

1. Criar e ativar venv (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instalar dependências da aula 20 (exemplo):

```bash
cd aula-20
pip install --upgrade pip
pip install -r requirements.txt
```

Observação: algumas pastas (ex.: `aula-19`, `aula-20`) também podem ter seu próprio `requirements.txt` — instale conforme a pasta que for testar.

Executar a aplicação (para testes funcionais/E2E)
```bash
cd aula-20
python run.py
# abre em http://localhost:5000
```

Executar testes
---------------
- Rodar todos os testes da aula 20:
```bash
cd aula-20
pytest -q
```
- Rodar apenas os E2E (necessário chromedriver ou webdriver-manager):
```bash
cd aula-20
pytest tests/e2e -q
```

Requisitos para E2E
- Tenha um WebDriver compatível (chromedriver) no PATH ou instale `webdriver-manager` e adapte os testes.
- O servidor (`python run.py`) deve estar rodando em `http://localhost:5000` antes de executar os testes E2E.

Qualidade de código
-------------------
Os comandos usados pela pipeline (e que você deve rodar localmente) são:

```bash
black --check .
flake8 .
pytest
```

CI/CD
-----
Existem workflows configurados para a aula 16 e 20 em:

- `.github/workflows/ci-aula-16.yml`
- `.github/workflows/ci-aula-20.yml`

Ambos rodam `pytest`, `flake8` e `black --check` a cada push/PR que altere a pasta correspondente.

Evidência de TDD
--------------------------------
Observação: não há prints nem commits anexados neste repositório; abaixo descrevo, em texto, o ciclo RED → GREEN → REFACTOR realizado para implementar `search_users`.

1) RED — adicionar testes que falham
	- Arquivos de teste criados com comportamento esperado (falhavam inicialmente):
	  - `aula-20/tests/unit/test_user_search.py` (vários cenários de busca)
	  - `aula-20/tests/integration/test_user_search_route.py` (teste da rota `GET /users?name=`)
	- Esses testes definem o contrato: busca por substring, case-insensitive, trimming de espaços, e comportamento para string vazia.

2) GREEN — implementar o mínimo para passar os testes
	- Implementação adicionada: `aula-20/app/services/user_services.py` → `search_users(name)` que filtra `users` por substring (case-insensitive) e trata `""`/`None`.
	- Ajuste de rota: `aula-20/app/routes/user_routes.py` passou a aceitar o query param `name` e delegar para `search_users` quando presente.
	- Resultado: os testes unitários e de integração foram executados e passaram após essa implementação mínima.

3) REFACTOR — melhorar sem alterar comportamento
	- Refatorações pequenas aplicadas: `strip()` do nome pesquisado, normalização para `lower()` e limpeza do código onde aplicável.
	- API e contratos mantidos.

