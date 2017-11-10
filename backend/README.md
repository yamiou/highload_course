# backend

## search api

### start
```
pip install -r requirements.txt
python runner.py api_app
```

### Nginx config

```
location ^~ /api/ {
			proxy_pass http://localhost:7080/;
}
```
