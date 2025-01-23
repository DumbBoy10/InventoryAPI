# Inventory management API for website

Tenhle projet je rozpracovaná API pro správu skladu. API je napsané v Pythonu s využitím frameworku FastAPI. Data jsou ukládána do PostgreSQL databáze.


### Live api:
[https://invapi.marian-janek.com/](https://invapi.marian-janek.com/)
#### Stažení pro postman: `(Doporučuji pro jednodušší shlednutí funkcnosti)`
[Zde](InventoryAPI.postman_collection.json)


## Instalace (Doporucuji live demo server)

1. Naklonujte si tento repozitář
2. Vytvořte si virtuální prostředí
3. Nainstalujte si potřebné balíčky pomocí příkazu `pip install -r requirements.txt`
4. Vytvořte si databazi v PostgreSQL a vytvořte v ní tabulky (tabulky jsou popsány v souboru `models.py`)
5. Vytvořte si soubor `.env` a nastavte si v něm proměnné `DATABASE_URL` a `SECRET_KEY`
6. Spusťte aplikaci pomocí příkazu `uvicorn main:app --host 127.0.0.1 --port 8000`

## Použití

API obsahuje následující endpointy:

### Autentizace
- `POST /auth/register` - registrace nového uživatele
- `POST /auth/login` - přihlášení uživatele
- `GET /auth/me` - získání informací o přihlášeném uživateli
### Kategorie
- `GET /category` - získání všech kategorií
- `POST /category` - vytvoření nové kategorie
- `GET /category/update/` - aktualizace kategorie
- `GET /category/delete/` - smazání kategorie
### Položky
- `GET /items` - získání všech položek
- `POST /items` - vytvoření nové položky
- `GET /items/item/` - získaní položky podle ID
- `GET /items/update/` - aktualizace položky
- `GET /items/delete/` - smazání položky

- `GET /items/add_stock` - přidání zásob (množství) k položce podle ID (pro odebírání zásob je třeba zadat záporné číslo)
### Logy
- `GET /log` - získání všech logů

## Detaily endpointů

### POST / auth/register
Registrace nového uživatele do systému.

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                                   |
|-----------:|:----------:|:------:|---------------------------------------------------------|
| `username` |    ano     | string | Uživatelské jméno.                                      |
|    `email` |    ano     | string | Email uživatele.                                        |
| `password` |    ano     | string | Heslo uživatele.                                        |

**Response**

```
{
    "message": "User registered.",
    "user": { ... }
}
```

---

### POST / auth/login
Přihlášení uživatele do systému.

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                                   |
|-----------:|:----------:|:------:|---------------------------------------------------------|
| `username` |    ano     | string | Uživatelské jméno.                                      |
| `password` |    ano     | string | Heslo uživatele.                                        |

**Response**

```
{
    "access_token": "<token>",
    "token_type": "bearer"
}
```

---

### GET / auth/me
Získání informací o aktuálně přihlášeném uživateli.

**Parametry**

Žádné.

**Response**

```
{
    "password": <password>,
    "id": 4,
    "created_at": "2025-01-21T19:36:16.596624",
    "username": "Test",
    "email": "test@test.com",
    "role": "admin",
    "updated_at": "2025-01-21T19:36:16.596624"
}
```

---

### GET / category
Výpis všech kategorií.

**Parametry**

Žádné.

**Response**

```
[
    {
        "id": 1,
        "created_at": "2025-01-21T18:52:09.948755",
        "description": "Description 1",
        "name": "Category 1",
        "updated_at": "2025-01-21T18:52:09.948755"
    },
    {
        "id": 2,
        "created_at": "2025-01-21T18:53:15.609222",
        "description": "Description 2",
        "name": "Category 2",
        "updated_at": "2025-01-21T18:53:15.609222"
    }
]
```

---

### POST / category
Vytvoření nové kategorie (Admin only).

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                                   |
|-----------:|:----------:|:------:|---------------------------------------------------------|
|    `name`  |    ano     | string | Název kategorie.                                        |
| `description` |  ne      | string | Popis kategorie.                                        |

**Response**

```
{
    "message": "Category has been created",
    "category": { ... }
}
```

---

### PUT / category/update
Aktualizace kategorie (Admin only).

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                                   |
|-----------:|:----------:|:------:|---------------------------------------------------------|
| `category_id` |    ano  |  int   | ID kategorie.                                           |
|    `name`  |    ne      | string | Nový název kategorie.                                   |
| `description` |  ne      | string | Nový popis kategorie.                                   |

**Response**

```
{
    "message": "Category {category_id} has been updated",
    "category": { ... }
}
```

---

### DELETE / category/delete
Smazání kategorie (Admin only).

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                                   |
|-----------:|:----------:|:------:|---------------------------------------------------------|
| `category_id` |    ano  |  int   | ID kategorie k odstranění.                              |

**Response**

```
{
    "message": "Category {category_id} has been deleted"
}
```

---
### GET / items
Výpis položek podle filtru.

**Parametry**

|      Název   | Požadováno |  Typ   | Popis                                                   |
|-------------:|:----------:|:------:|---------------------------------------------------------|
| `category_id`|     ne     |  int   | ID kategorie pro filtrování položek.                   |
|   `search`   |     ne     | string | Hledaný řetězec pro vyhledávání položek.               |
|    `limit`   |     ne     |  int   | Počet položek k zobrazení (výchozí 100).               |
|   `offset`   |     ne     |  int   | Počet přeskočených položek (výchozí 0).                |

**Response**

```
[
    {
        "description": "Description 1",
        "name": "Name 1",
        "quantity": 100,
        "price": 799.9,
        "updated_at": "2025-01-21T20:42:32.835464",
        "id": 1,
        "category_id": 1,
        "created_at": "2025-01-21T20:42:32.835464"
    },
    {
        "description": "Description 2",
        "name": "Name 2",
        "quantity": 100,
        "price": 799.9,
        "updated_at": "2025-01-21T20:42:32.835464",
        "id": 2,
        "category_id": 1,
        "created_at": "2025-01-21T20:42:32.835464"
    }
]
```

---
### POST / items
Vytvoření nové položky.

**Parametry**

|      Název   | Požadováno |  Typ   | Popis                                                   |
|-------------:|:----------:|:------:|---------------------------------------------------------|
|    `name`    |     ano    | string | Název položky.                                         |
| `description`|     ne     | string | Popis položky.                                         |
| `category_id`|     ano    |  int   | ID kategorie, do které položka patří.                  |
|  `quantity`  |     ano    |  int   | Počet kusů skladem.                                    |
|    `price`   |     ano    | float  | Cena položky.                                          |

**Response**

```
{
    "message": "Item has been created.",
    "item": { ... }
}
```

---
### GET / items/item
Výpis položky podle ID.

**Parametry**

|      Název   | Požadováno |  Typ   | Popis                                                   |
|-------------:|:----------:|:------:|---------------------------------------------------------|
|    `item_id` |     ano    |  int   | ID požadované položky.                                  |

**Response**

```
{
    "name": "Name 1",
    "description": "Description 1",
    "quantity": 100,
    "price": 799.9,
    "updated_at": "2025-01-21T20:42:32.835464",
    "id": 1,
    "category_id": 1,
    "created_at": "2025-01-21T20:42:32.835464"
}
```

---
### PUT / items/update
Úprava položky.

**Parametry**

|      Název   | Požadováno |  Typ   | Popis                                                   |
|-------------:|:----------:|:------:|---------------------------------------------------------|
|    `item_id` |     ano    |  int   | ID položky k úpravě.                                   |
|    `name`    |     ne     | string | Nový název položky.                                    |
| `description`|     ne     | string | Nový popis položky.                                    |
| `category_id`|     ne     |  int   | Nový ID kategorie položky.                             |
|  `quantity`  |     ne     |  int   | Nový počet kusů skladem.                               |
|    `price`   |     ne     | float  | Nová cena položky.                                     |

**Response**

```
{
    "message": "Item {item_id} has been updated.",
    "item": { ... }
}
```

---

### DELETE / items/delete
Smazání položky.

**Parametry**

|      Název   | Požadováno |  Typ   | Popis                                                   |
|-------------:|:----------:|:------:|---------------------------------------------------------|
|    `item_id` |     ano    |  int   | ID položky k odstranění.                                |

**Response**

```
{
    "message": "Item {item_id} has been deleted."
}
```

---

### POST / items/add_stock
Přidání nebo odebrání zásob (minusové hodnoty pro odebrání).

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                                   |
|-----------:|:----------:|:------:|---------------------------------------------------------|
|  `item_id` |    ano     |  int   | ID položky.                                             |
| `quantity` |    ano     |  int   | Množství k přidání nebo odebrání (záporná hodnota).     |

**Response**

```
{
    "message": "{quantity} has been added to Item {item_id} stock.",
    "item": { ... }
}
```
---
### POST / log
Přidání nebo odebrání zásob (minusové hodnoty pro odebrání).

**Parametry**

|      Název | Požadováno |  Typ   | Popis                                       |
|-----------:|:----------:|:------:|---------------------------------------------|
|  `limit` |     ne     |  int   | Počet položek k zobrazení (výchozí 100).    |
| `offset` |     ne     |  int   | Počet přeskočených položek (výchozí 0).     |

**Response**

```
[
    {
        "id": 1,
        "action": "Added 100 to Item 1 stock.",
        "timestamp": "2025-01-23T16:16:19.175934",
        "user_id": 4,
        "item_id": 1,
        "quantity": 100
    },
    {
        "id": 2,
        "action": "Added 100 to Item 2 stock.",
        "timestamp": "2025-01-23T16:16:25.352056",
        "user_id": 4,
        "item_id": 1,
        "quantity": 100
    }
]
```
---
