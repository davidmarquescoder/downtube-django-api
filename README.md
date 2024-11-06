# Installing and configuring the project

#### Creating python virtual environment
``` shell
python -m venv venv
```

#### Activating python virtual environment
``` shell
./venv/Scripts/Activate.ps1
```

---

#### Installing all dependencies
``` shell
pip install -r requirements.txt
```

#### Updating dependencies
If any new dependencies are added to the project, run the following command

``` shell
pip freeze > requirements.txt
```

---

#### Bringing up the server
On my machine I'm not able to run the server on django's default port (8000). Perhaps this port is already being used for another purpose, so let's run it on port 3333.

``` shell
python manage.py runserver 3333
```

---
#### Routes

Route to download a youtube video:

- `GET download/?video_url=https://MeuLinkDoYoutube.com`

Example of use:

- `http://localhost:3333/download/?video_url=https://www.youtube.com/watch/?v=Hr1UrJfzJ54`