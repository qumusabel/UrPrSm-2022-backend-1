### **Intro**

Компании JINGU Digital необходимо разработать сервис для сокращения ссылок, который позволит укорачивать длинные ссылки в интернете. Так как JINGU еще не успела привлечь раунд инвестиций под этот стартап, MVP сервиса придется реализовывать без фронтенда.

Сервис должен принимать полный адрес ссылки, сокращать его до вида `http://адрес_вашего_сервера/xxxxxxxx` , сохранять в базу данных информацию об исходной и сокращенной ссылке и отдавать пользователю полную ссылку, по запросу, через сокращенную ссылку. Также сервис должен отслеживать количество переходов по сокращенной ссылке.

### **API**

### **1) POST `/shorten`**

Принимает на вход длинную ссылку, а в ответ отдает сгенерированный короткий адрес, по которому можно будет получить доступ к исходной ссылке

**Request**

`Content-type: json`

`{
    "urlToShorten": string;
}`

**Response**

`Content-type: json`

`{
    "status": string;
    "shortenedUrl": string;
}`

**Пример**

POST `http://localhost:3000/shorten`

`{
    "urlToShorten": "https://www.jingu.ru/sirius/backend-rest"
}`

=> 201 Response (Created)

`{
    "status": "Created",
    "shortenedUrl": "http://localhost:3000/1b9d6bcd"
}`

---

### **2) GET `/:url`**

Принимает сокращенный адрес ссылки в качестве query-параметра, а в ответ перенаправляет пользователя на исходную ссылку

**Request**

`url: string;`

**Response**

`Content-type: json`

`{
    "redirectTo": string;
}`

**Пример**

GET `http://localhost:3000/1b9d6bcd`

=> 301 Response (Moved permanently)

`{
    redirectTo: 'https://www.jingu.ru/sirius/backend-rest',
}`

HTTP Headers

```
...
location: https://www.jingu.ru/sirius/backend-rest
...

```

### **3) GET `/:url/views`**

Принимает сокращенный адрес ссылки в качестве query-параметра, а в ответ возвращает количество просмотров заданной сокращенной ссылки

**Request**

`url: string;`

**Response**

`Content-type: json`

`{
    "viewCount": string;
}`

**Пример**

GET `http://localhost:3000/1b9d6bcd/views`

=> 200 Response (OK)

`{
    "viewCount": 2,
}`

## **Дополнительно**

Для создания случайного токена, можно использовать любую библиотеку, например, [nanoid](https://github.com/ai/nanoid/)
