# cor-iesu

## run

```bash
flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' run
```


## migrate

```bash
flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' db migrate
flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' db upgrade
```
