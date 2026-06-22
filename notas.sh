# 1. Crea la carpeta del proyecto
mkdir carnets_app && cd carnets_app

# 2. Crea entorno virtual
python -m venv venv

# 3. Actívalo
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# 4. Instala Django y el driver de PostgreSQL
pip install django psycopg2-binary pillow
###--------------------------#################
# 1. Crea el proyecto
django-admin startproject config .

# 2. Crea la app carnets
python manage.py startapp carnets


#ruta de postgreSQL agregar a la variables de entorno PATH
C:\Program Files\PostgreSQL\18\bin

#error en la consola
psql (18.1)
ADVERTENCIA: El código de página de la consola (850) difiere del código
            de página de Windows (1252).
            Los caracteres de 8 bits pueden funcionar incorrectamente.
            Vea la página de referencia de psql «Notes for Windows users»
            para obtener más detalles.
#SOLUCION ES cambiar la codificación de la consola a UTF-8 CON
chcp 1252

#crear base de datos Conéctate como postgres
psql -U postgres
#Crea el usuario primero
CREATE USER carnets_user WITH PASSWORD 'tu_password_seguro';
ALTER ROLE carnets_user SET client_encoding TO 'utf8';
ALTER ROLE carnets_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE carnets_user SET timezone TO 'UTC';
#2 Crea la BD ya asignándole el dueño
CREATE DATABASE carnets_db OWNER carnets_user;
#3 Dale permisos
GRANT ALL PRIVILEGES ON DATABASE carnets_db TO carnets_user;






# 1. Crea las migraciones
python manage.py makemigrations

# 2. Aplica las migraciones a PostgreSQL
python manage.py migrate

# 3. Crea superusuario para entrar al admin
python manage.py createsuperuser



http://127.0.0.1:8000/plantilla/1/editar/