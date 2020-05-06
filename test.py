from requests import get

host = 'http://127.0.0.1/api/'
token_lunar = '35QE6WdVcx3jfFHcUi5euw'
token_admin = '-UbIxK-rP5N4r0cYhb12HA'

pss = 'pbkdf2:sha256:150000$PZDpxSd1$c14d97a8717d8bd02acc1c3926301fc5fac8768d76eceaa838a1c94b61a0a577'

url = host + token_admin + '/users/' + 'admin'

print(url)
print(get(url).json())

