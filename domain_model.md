# Domain Model

## Entities

### User
Пользователь сервиса.

### Company
Компания пользователя.

### Product
Товар компании, для которого можно получать коды.

### CodeRequest
Запрос на получение кодов для конкретного товара.

### Code
Код маркировки, полученный в результате запроса.

## Relations

User
- id
- email
- password_hash
- created_at

Company
- id
- name
- created_at

CompanyMember
- id
- user_id
- company_id
- role

Product
- id
- name
- company_id

CodeRequest
- id
- product_id
- created_by
- quantity
- status
- created_at

Code
- id
- code_request_id
- value

## Ограничения

User.email
→ NOT NULL
→ UNIQUE

Product.company_id
→ NOT NULL
→ FK → Company.id

CodeRequest.product_id
→ NOT NULL
→ FK → Product.id

CodeRequest.created_by
→ NOT NULL
→ FK → User.id

CodeRequest.quantity
→ NOT NULL
→ >= 1

CodeRequest.status
→ NOT NULL
→ waiting / processing / failed / completed

Code.code_request_id
→ NOT NULL
→ FK → CodeRequest.id

Code.value
→ NOT NULL