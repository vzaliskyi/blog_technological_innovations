# Product overview

**Розроблюваний проєкт - веб-сайт "Блог огляду новинок техніки".** 
  
Приблизний опис функціоналу:
	Додаток призначений для користувачів, які хочуть першими дізнаватися про новинки техніки(смартфони, ноутбуки, планшети та ін.) або існуючі девайси.
Користувач зможе прочитати короткий опис функціоналу та основних характеристик пристрою, побачити фото і дізнатися фідбек про продукт. 
 	На сайті буде передбачена можливість реєстрації. Зареєстрований користувач,буде мати сторінку власного профілю та зможе писати власні публікації.  Не менш важливою є комунікація між користувачами. Тому користувач матиме можливість оцінити сподобався йому огляд чи ні, та написати коментар.
 
## Stack technologies: flask, python, html, css, sqlite, bootstrap.

* Trello - https://trello.com/b/zvIob6WD/blog-an-overview-of-new-tech-products
* Roadmap - https://drive.google.com/file/d/1OBWLyoox4YvS2Rc_xrFGwUw-fkbWV745/view?usp=sharing
* Estimates - https://docs.google.com/spreadsheets/d/1b2Ev-5K4YolZTeYkVMPcZzPE_FU_9bCz62ri6uFccoI/edit?usp=sharing
* CI server -  https://app.circleci.com/pipelines/github/dima-yurchuk/blog_technological_innovations
* Architectural diagram -  https://drive.google.com/file/d/137Cw_mAKtq2IZ_AVsyWadZNN4FSjOYEO/view?usp=sharing
* ER-diagram -  https://drive.google.com/file/d/1bN7CuCRblA6oAfSTkFle_BEPFeQRkJja/view

## Code styling:
У python коді старатися дотримуєтися стандарту PEP-8:
https://www.python.org/dev/peps/pep-0008

* рядкові коментарі починаємо з пробілу
* спочку імпортуємо власні моді, потім імпортуємо готові модулі python
* імпорти пакетів робимо окремим рядком(крім імпортів модулі з пакетів)
* максимальна кількість символів у рядку - 79
* функції і класи зверху обмежуємо двома пробілами
* рядки беремо в одинарні лапки(але якщо рядок містить апостроф використовуємо подвійні лапки) 
* назви змінних - snake_case 
* назви - класів CapWords
* назви функцій, методів - snake_case 
* для відступів використовуємо 4 пробіли
* оператори оточуємо 1 пробілом
* методи в класі оточені одним порожнім рядком
## Branching policy:
Ми маємо основний репозиторій з однією віткою master. При виконанні завдань девелопери роблять fork головного репозиторію. Після виконання завдання виконується pull request, після чого відбувається merge з гілкою master.
## Setup:
* python3 -m venv env python -m venv env
* Unix Bash:  source env/bin/activate          
* Windows: env\Scripts\activate.bat          env\Scripts\deactivate.bat
* pip install -r requirements.txt
* flask run
