#Flask API

     Flask, Flask-RESTful, SQLAlchemy

Heroku: https://afternoon-river-16729.herokuapp.com/

ТЗ:

    Необходимо написать http-сервис с помощью Flask и развернуть его на сервере, например, heroku (можно захостить и на другом). 
    Приложение должно предоставлять API, позволяющее:
       - проходить регистрацию и авторизовываться (тип авторизации - Basic Auth); 
       - видеть все опубликованные посты (без авторизации); 
       - публиковать, редактировать, удалять только свои посты (только с авторизацией); 
       - публиковать, редактировать и удалять только свои комментарии под постами (только с авторизацией).

Описание api:

1. /api/v1/users

       - GET: информация о зарегистрированных пользователях (доступна только для пользователя - admin)
       - POST: регистрация нового пользователя (тип авторизации - Basic Auth)
     
        формат:
            {
               "username": "user",
               "email": "user@mail.ru",
               "password": "password"
            }

2. /api/v1/users/<int:user_id> (доступно для самого пользователя и админа)

         - GET: информация о зарегистрированном пользователе с id = user_id 
         - DELETE: удалить пользователя 

3. /api/v1/posts

         - GET: список всех постов (доступен всем пользователям)
         - POST: добавление нового поста (доступно для зарегистрированных и авотризованных поьзователей)

           формат:
               {
                  "title": "title",
                  "content": "content"
               }

4. /api/v1/posts/<int:post_id>

         - GET: информация о посте с id = post_id (доступно всем пользователям)
         - PATCH: редактирование поста с id = post_id (доступно только если пост принадлежит авторизованному пользователю)
         - DELETE: удаление поста с id = post_id  (доступно только если пост принадлежит авторизованному пользователю)

5. /api/v1/comments

         - GET: список всех комментариев (доступен всем пользователям)
         - POST: добавление нового комментария под постом (доступно для зарегистрированных и авотризованных поьзователей)

           формат:
              {
                 "title": "title",
                 "content": "content"
              }
    
6. /api/v1/comments/<int:comment_id>

       - GET: информация о комментарии с id = comment_id (доступно всем пользователям)
       - PATCH: редактирование комментария с id = comment_id (доступно только если комментарий принадлежит авторизованному пользователю)
       - DELETE: удаление комментария с id = comment_id  (доступно только если комментарий принадлежит авторизованному пользователю)
    
Разворачиваем проект локально:

1. Скачайте репозиторий

2. Создайт виртуальное окружение:

       python -m venv env

3.Активируйте виртуальное окружение:

     source env/bin/activate

4.Чтобы установить все требуемые библиотеки python в новом окружении выполните команду:

     pip install -r requirements.txt

5.Если у вас macOS до выполнения команды pip install -r requirements.txt выполните команду:

     env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.8.4      
     
     Для предотвращения появления ошибки (error: command 'gcc' failed with exit status 1.) при установке зависимостей.

6.Запустите сервер командой:

     python -m flask run

7.Приложение будет доступно по пути: http://127.0.0.1:5000/

