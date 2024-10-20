# Instalando e Configurando o projeto

#### Criando Ambiente virtual python
``` shell
python -m venv venv
```

#### Ativando Ambiente virtual python
``` shell
./venv/Scripts/Activate.ps1
```

---

#### Instalando todas as dependências
``` shell
pip install -r requirements.txt
```

#### Atualizando as dependências
Se for adicionado alguma nova depedência ao projeto, rode o comando abaixo

``` shell
pip freeze > requirements.txt
```

---

#### Subindo o server
Na minha máquina não estou conseguindo rodar o server na porta padrão do django (8000) talvez essa porta já esteja sendo usada para outra finalidade, então vamos rodar na porta 3333.

``` shell
python manage.py runserver 3333
```

---
#### Rotas

Rota para fazer download de um vídeo do youtube:

- `GET download/?video_url=https://MeuLinkDoYoutube.com`

Exemplo de uso:

- `http://localhost:3333/download/?video_url=https://www.youtube.com/watch/?v=Hr1UrJfzJ54`