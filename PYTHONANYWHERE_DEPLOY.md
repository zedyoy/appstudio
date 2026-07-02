# Deploy su PythonAnywhere gratis

Questa e la strada piu semplice per usare l'app da PC, tablet e smartphone con
un link privato tipo:

```text
https://Veyoy.pythonanywhere.com
```

## 1. Porta il progetto su PythonAnywhere

Metodo consigliato: repo GitHub privato.

Sul tuo PC:

```bash
git add .
git commit -m "Versione studio per PythonAnywhere"
git remote add origin https://github.com/zedyoy/appstudio.git
git push -u origin main
```

Su PythonAnywhere, apri **Bash** e fai:

```bash
cd ~
git clone https://github.com/zedyoy/appstudio.git
cd appstudio
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p instance
```

Se il repo e privato, GitHub ti chiedera username e token personale.

## 2. Crea la web app

Da PythonAnywhere:

1. Vai su **Web**.
2. Clicca **Add a new web app**.
3. Scegli il dominio gratuito `Veyoy.pythonanywhere.com`.
4. Scegli **Manual configuration**.
5. Scegli la stessa versione Python usata per il virtualenv, per esempio 3.10.

Nella sezione **Code** imposta:

```text
Source code: /home/Veyoy/appstudio
Working directory: /home/Veyoy/appstudio
Virtualenv: /home/Veyoy/appstudio/venv
```

Nella sezione **Static files** aggiungi:

```text
URL: /static/
Directory: /home/Veyoy/appstudio/static
```

## 3. Configura il file WSGI

Sempre nella pagina **Web**, clicca sul file WSGI e sostituisci il contenuto
con quello in:

```text
deploy/pythonanywhere_wsgi.py
```

Poi cambia:

```python
USERNAME = "Veyoy"
PROJECT_DIR = "/home/Veyoy/appstudio"
os.environ.setdefault("SECRET_KEY", "una-stringa-lunga-casuale")
os.environ.setdefault("APP_PASSWORD", "la-password-che-userai-per-entrare")
```

Non mettere questa password su GitHub.

## 4. Ricarica

Torna nella pagina **Web** e premi:

```text
Reload
```

Poi apri:

```text
https://Veyoy.pythonanywhere.com
```

Ti dovrebbe comparire la schermata login dell'app.

## 5. Backup progressi

I progressi sono salvati qui:

```text
/home/Veyoy/appstudio/instance/user_progress.db
```

Ogni tanto fai un backup da Bash:

```bash
cd ~/appstudio
mkdir -p backups
cp instance/user_progress.db backups/user_progress_$(date +%F).db
```

Se usi molto la funzione "Salva domanda", fai backup anche dei database in
`data/`, per sicurezza.

## 6. Aggiornare l'app dopo modifiche

Da Bash su PythonAnywhere:

```bash
cd ~/appstudio
git pull
source venv/bin/activate
pip install -r requirements.txt
```

Poi vai su **Web** e premi **Reload**.

Se `git pull` si lamenta per database modificati, prima fai backup della cartella
`data/`, poi decidi se tenere i file online o sostituirli con quelli nuovi.
