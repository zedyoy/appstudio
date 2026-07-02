# Deploy privato

L'app ora e pronta per un deploy personale: usa `APP_PASSWORD` per bloccare
l'accesso e `PROGRESS_DB_PATH` per salvare i progressi in un database SQLite
persistente.

## Variabili d'ambiente

```text
SECRET_KEY=una-stringa-lunga-casuale
APP_PASSWORD=la-tua-password
PROGRESS_DB_PATH=/app/instance/user_progress.db
```

In locale `APP_PASSWORD` puo restare vuota: la schermata login si attiva solo
quando la variabile e impostata.

## Comando di avvio

```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

Se usi Docker:

```bash
docker build -t quiz-uni .
docker run -p 5000:5000 \
  -e SECRET_KEY=dev-change-me \
  -e APP_PASSWORD=la-tua-password \
  -v quiz_progress:/app/instance \
  quiz-uni
```

## Persistenza

I database delle materie restano in `data/`. I progressi personali finiscono in
`instance/user_progress.db` o nel percorso indicato da `PROGRESS_DB_PATH`.
Sul servizio di hosting serve quindi un disco/volume persistente montato su
`/app/instance`, altrimenti i progressi possono sparire a ogni redeploy.

Nello stesso database vengono salvati anche la sessione attiva, la materia
selezionata, la coda corrente, gli XP, la combo e la missione di sessione.

## Strada consigliata

Per usarla da tablet, PC e smartphone senza tenere acceso il computer di casa,
la strada piu semplice per uso personale e PythonAnywhere.

### PythonAnywhere gratis

Vedi la guida completa:

```text
PYTHONANYWHERE_DEPLOY.md
```

In breve:

1. Metti il progetto su GitHub privato.
2. Clonalo su PythonAnywhere.
3. Crea una web app Flask con configurazione manuale.
4. Copia il contenuto di `deploy/pythonanywhere_wsgi.py` nel file WSGI.
5. Imposta `APP_PASSWORD`, `SECRET_KEY` e `PROGRESS_DB_PATH`.
6. Premi Reload.

Per uso single-user va bene iniziare dal piano gratuito. Tieni solo d'occhio lo
spazio disponibile e fai backup di `instance/user_progress.db`.

### Alternative con volume persistente

Se in futuro vuoi una soluzione piu solida:

1. Metti il repo su GitHub, anche privato.
2. Deploy su un servizio che supporta app Python/Docker e volumi persistenti.
3. Imposta `APP_PASSWORD` e `SECRET_KEY`.
4. Monta un volume su `/app/instance`.
5. Imposta `PROGRESS_DB_PATH=/app/instance/user_progress.db`.

Opzioni adatte:

- Render: piu semplice da pannello, ma il disco persistente e disponibile sui
  web service a pagamento. Docs: https://render.com/docs/disks
- Fly.io: ottimo con Dockerfile e volume, piu tecnico ma solido. Docs:
  https://fly.io/docs/volumes/overview/
- Railway: comodo se vuoi partire veloce, con volume per servizio. Docs:
  https://docs.railway.com/volumes/reference

Per questa app single-user va bene SQLite con volume. Non scalare a piu repliche:
con SQLite deve restare una sola istanza che scrive sullo stesso file.
