# NovaRent - Laboratorio U5

Proyecto base en Python del Equipo 7 - NovaRent.

## Funcionalidades

- Confirmación de pedidos con validación de total y estado.
- Descuento del 15 % para clientes VIP.
- Rechazo de confirmación cuando el cliente tiene deuda pendiente.
- Servicio de checkout conectado a una pasarela de pago.
- Persistencia de pedidos mediante SQLAlchemy.
- Cancelación permitida al propietario durante las primeras 24 horas.
- Cancelación administrativa, excepto cuando el pedido ya fue enviado.

## Requisitos

- Python 3.11 o superior (el código utiliza `datetime.UTC`).
- `pip`.

Las dependencias del proyecto se encuentran en [`requirements.txt`](requirements.txt):
Pytest, Pytest-Cov, SQLAlchemy y Ruff.

## Instalación

Desde la carpeta `Proyecto_Python_Base_U5`, crea y activa un entorno virtual:

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Estructura del proyecto

```text
Proyecto_Python_Base_U5/
├── src/
│   ├── application.py  # Servicio de checkout y cobro
│   ├── domain.py       # Entidad Order y reglas de negocio
│   ├── repository.py   # Modelo SQLAlchemy y repositorio
│   └── security.py     # Reglas para cancelar pedidos
├── tests/
│   ├── test_order.py
│   ├── test_repository.py
│   ├── test_security.py
│   └── test_service.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Uso básico

### Confirmar un pedido

```python
from src.domain import Order

order = Order(total=100, vip=True)
amount = order.confirm()

print(amount)        # 85.0
print(order.status)  # CONFIRMED
```

Un pedido no puede confirmarse dos veces, debe tener un total positivo y no
puede confirmarse si el cliente tiene deuda:

```python
from src.domain import CustomerHasDebt, Order

try:
    Order(total=100).confirm(customer_debt=50)
except CustomerHasDebt:
    print("El pedido no puede confirmarse por deuda pendiente")
```

### Procesar un checkout

`OrderService` recibe un objeto que expone `charge(amount)` como pasarela de
pago. Si el cobro falla, el pedido queda en estado `REJECTED`.

```python
from src.application import OrderService
from src.domain import Order


class PaymentGateway:
    def charge(self, amount):
        return True


order = Order(total=200, vip=True)
amount = OrderService(PaymentGateway()).checkout(order)

print(amount)        # 170.0
print(order.status)  # CONFIRMED
```

### Persistir un pedido

El repositorio usa una sesión de SQLAlchemy. `make_engine()` crea por defecto
una base SQLite en memoria y las tablas necesarias.

```python
from sqlalchemy.orm import Session

from src.domain import Order
from src.repository import SqlOrderRepository, make_engine

engine = make_engine()
with Session(engine) as session:
    SqlOrderRepository(session).save(1, Order(total=120))
    session.commit()
```

### Validar cancelaciones

```python
from datetime import UTC, datetime, timedelta

from src.security import can_cancel

now = datetime.now(UTC)
allowed = can_cancel(
    status="NEW",
    owner_id=10,
    user_id=10,
    is_admin=False,
    created_at=now - timedelta(hours=1),
    now=now,
)
```

La función devuelve `False` para pedidos enviados, usuarios que no son
propietarios o solicitudes fuera de la ventana de 24 horas. Un administrador
puede cancelar pedidos no enviados.

## Pruebas

Ejecuta toda la suite con:

```bash
python -m pytest -v
```

Para ejecutar un archivo específico:

```bash
python -m pytest tests/test_order.py -v
```

Para generar un informe de cobertura:

```bash
python -m pytest --cov=src --cov-report=term-missing --cov-report=html
```

El informe HTML se genera en `htmlcov/`.

## Calidad del código

La configuración de Ruff se encuentra en [`pyproject.toml`](pyproject.toml) y
usa una longitud máxima de línea de 100 caracteres. Para revisar el código:

```bash
ruff check .
```

## Estado del proyecto

Este repositorio corresponde a una base de laboratorio para la Unidad 5. No
incluye una interfaz de línea de comandos ni un servidor web; los componentes
se ejecutan desde Python y se validan mediante la suite de pruebas.
