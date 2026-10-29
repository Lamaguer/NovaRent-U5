import pytest

from src.domain import CustomerHasDebt, Order


def test_vip_discount():
    o = Order(100, vip=True)
    assert o.confirm() == 85
    assert o.status == "CONFIRMED"

#Prueba con total de 200 buckaroos y Cliente VIP, resultado esperado 170.
def test_vip_discount2():
    o = Order(200, vip=True)
    assert o.confirm() == 170
    assert o.status == "CONFIRMED"

def test_regular_no_discount():
    assert Order(100).confirm() == 100

#Prueba con total de 200 buckaroos y Cliente regular, Resultado esperado 200.
def test_regular_no_discount2():
    assert Order(200).confirm() == 200

def test_customer_debt():
    with pytest.raises(CustomerHasDebt):
        Order(100).confirm(customer_debt=50)

@pytest.mark.parametrize("total", [0, -1])
def test_invalid_total(total):
    with pytest.raises(ValueError):
        Order(total).confirm()

def test_cannot_confirm_twice(): 
    order = Order(100) 
    order.confirm() 
    with pytest.raises(ValueError, match="Already confirmed."): 
        order.confirm() 
#python -m pytest tests/test_order.py -v
#python -m pytest tests/test_order.py::test_cannot_confirm_twice -v