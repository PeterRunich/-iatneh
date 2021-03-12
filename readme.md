# ieatneh
## Как запустить?
1. Все файлы должны находиться в папке с названием ieatneh
2. Установить библеотеки ```python -m pip install -r requirements.txt```
3. Установить переменную среды "TG_BOT_TOKEN"
   ```
   Для PowerShell $env:TG_BOT_TOKEN="Токен"
   Для CMD set=Токен
   Для Linux export TG_BOT_TOKEN=Токен
   ```
4. В командной строке ввести находясь в не папки ieatneh
```python -m iatneh.app.main```
*При использовании CMD следует запускать от имени администратора
