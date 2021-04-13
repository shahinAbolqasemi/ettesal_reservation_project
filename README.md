# Reservation

---

This project belongs to the EttesalYekparche company, that has provided APIs for requesting meeting rooms, etc.

# Quick start

---

**1.** First install requirement packages with:
```
python -m pip install -r requirements
```

**2.** Set DATABASES and SECRET_KEY configurations in ```reservation_project/local_settings.py```

can use ```reservation_project/local_settings.py.sample```.
```python
SECRET_KEY = 'secret key'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'database_name',
    'USERNAME': 'username',
    'PASSWORD': 'password',
    'HOST': 'host',
    'PORT': 'port',
    } 
}
```