# SoproGest 🐾

MVP acadêmico de gestão de animais para a ONG Sopro da Vida (Biritiba Mirim/SP). Projeto demonstrativo, ainda não validado pela ONG.

## Funcionalidades implementadas
- Login administrativo com hash de senha.
- Cadastro e listagem de animais.
- Validação básica de campos e interface responsiva.
- Testes automatizados e workflow de CI no GitHub Actions.

**Fora do escopo desta versão:** módulos funcionais de doações e campanhas, implantação pública e validação em campo.

## Tecnologias
Python, Flask, SQLite, HTML e CSS.

## Como executar
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Acesse `http://127.0.0.1:5000`.

**Acesso apenas para demonstração local:** usuário `admin`, senha `TroqueEstaSenha123!`. Defina as variáveis de ambiente `ADMIN_PASSWORD` e `SECRET_KEY` antes de usar em qualquer ambiente compartilhado. Não publique a aplicação com as credenciais padrão.

## Testes
```bash
python -m pytest -q
```

## Limitações e segurança
Este MVP é uma demonstração acadêmica e **não deve ser exposto à internet** sem melhorias: CSRF, limitação de tentativas de login, gestão segura de credenciais, HTTPS, proteção de sessão, backups e revisão de permissões.

## Planejamento da validação
Testar com representante da ONG, mediante consentimento, as tarefas: acessar cadastro, cadastrar animal fictício e interpretar o resultado. Metas: 3/3 tarefas sem ajuda, cadastro em até 180 segundos e satisfação >= 4/5. Testes com usuários ainda não realizados.
