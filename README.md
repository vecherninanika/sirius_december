Онлайн платформа для обмена рецептами с использованием Fast Api
- Модели: Пользователи, Рецепты, Ингредиенты
- Платформа, где пользователи могут обмениваться рецептами блюд, делиться своим опытом приготовления и находить новые идеи для кулинарии.

Технологии проекта:
- прохождение flake8 + mypy в соответствии с конфигурациями проекта
- Кеширование через redis
- Метрики на время выполнения всех интеграционных методов (запросы в бд, редис и тп (гистограмма)

## API requests examples

### Authorization

- Register \
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username": "new", "code": 123456}'

- Login \
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username": "new user", "code": 123456}'

- Info \
curl -X POST http://127.0.0.1:8000/auth/info

- Delete \
curl -X POST http://127.0.0.1:8000/auth/delete_user/1 -H "Authorization: Bearer ACCESS_TOKEN"

- Update \
curl -X POST http://127.0.0.1:8000/auth/update_user/1 -H "Content-Type: application/json" -d '{"username": "new", "password": "new"}'

"/code/webapp/crud/crud.py   'NoneType' object is not subscriptable

Все возвращает 404.


### Ingredient

- Create \
curl -X POST http://127.0.0.1:8000/ingredient/create -H "Content-Type: application/json" -d '{"title": "new ingredient"}'

- Read \
curl -X GET http://127.0.0.1:8000/ingredient/read -H "Content-Type: application/json" -d '{"title": "new ingredient"}'

- Update \
curl -X POST http://127.0.0.1:8000/ingredient/update/1 -H "Content-Type: application/json" -d '{"title": "newt"}'

File "/code/webapp/crud/crud.py", line 51, in update
web                   |     await session.execute(update(model).where(model.id == id_).values(**data_dict))
web                   |                           ^^^^^^^^^^^^^^^^^^^
web                   | AttributeError: 'coroutine' object has no attribute 'where'


- Delete \
curl -X POST http://127.0.0.1:8000/ingredient/delete/1 -H "Content-Type: application/json"

File "/code/webapp/crud/crud.py", line 41, in delete
web                   |     await session.execute(delete(model).where(model.id == id_).returning(model.id))
web                   |                           ^^^^^^^^^^^^^^^^^^^
web                   | AttributeError: 'coroutine' object has no attribute 'where'


- Read all \
curl -X GET http://127.0.0.1:8000/ingredient/read_all -H "Content-Type: application/json"


### Recipe

- Create \
curl -X POST http://127.0.0.1:8000/recipe/create -H "Content-Type: application/json" -d '{"title": "new recipe", "ingredients": ["Water", "Pasta"]}'

- Read \
curl -X GET http://127.0.0.1:8000/recipe/read -H "Content-Type: application/json" -d '{"title": "new recipe"}'

- Update \
curl -X POST http://127.0.0.1:8000/recipe/update/1 -H "Content-Type: application/json" -d '{"title": "newt"}'

- Add ingredient \
curl -X POST http://127.0.0.1:8000/recipe/add_ingredient/1 -H "Content-Type: application/json" -d '{"ingredient": "Water"}'

- Delete \
curl -X POST http://127.0.0.1:8000/recipe/delete/1 -H "Content-Type: application/json"

- Read all \
curl -X GET http://127.0.0.1:8000/recipe/read_all -H "Content-Type: application/json"

- Find by ingredient \
curl -X GET http://127.0.0.1:8000/recipe/find_by_ingredient -H "Content-Type: application/json" -d '{"ingredient": "Pasta"}'

не работает 

- Read popular \
curl -X GET http://127.0.0.1:8000/recipe/read_popular -H "Content-Type: application/json"

404

- Read user recipes \
curl -X GET http://127.0.0.1:8000/recipe/read_user_recipes/1 -H "Content-Type: application/json"

404

- Add user \
curl -X GET http://127.0.0.1:8000/recipe/add_user/1 -H "Content-Type: application/json" -d '{"username": "new"}'

404 но я не знаю есть ли такой юзер



fixture не работают
update и delete не работают

Потом:
попробовать пагинацию
метрики
