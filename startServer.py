from os import system, name

defaultPort, clear_cmd = 8000, "cls" if name == "nt" else "clear"

port = input(f"Enter port (default {defaultPort}): ")

try:
  system(f"python manage.py makemigrations && python manage.py migrate && {clear_cmd} && python manage.py runserver 0.0.0.0:{port if port else defaultPort}")
except:
  system(f"python3 manage.py makemigrations && python3 manage.py migrate && {clear_cmd} && python3 manage.py runserver 0.0.0.0:{port if port else defaultPort}")
