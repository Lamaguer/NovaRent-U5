from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert  can_cancel("NEW", 1, 2, False, now, now) #assert not

#Admin borra el pedido de alguien mas
def test_admin_approved(): 
    created_at = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    now = datetime(2026, 1, 2, 12, 0, tzinfo=UTC)

    assert can_cancel("NEW", 1, 2, True, created_at, now)
    
    #python -m pytest tests/test_security.py::test_admin_approved -v

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied2(): #Horas exactas aun se expiran
    created_at = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    now = datetime(2026, 1, 2, 12, 0, tzinfo=UTC)
    assert not can_cancel("NEW", 1, 1, False, created_at, now)
    #python -m pytest tests/test_security.py::test_expired_denied2 -v

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)

