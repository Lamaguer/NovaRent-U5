from dataclasses import dataclass


class CustomerHasDebt(Exception):
    pass

@dataclass
class Order:
    total: float
    vip: bool = False
    status: str = "NEW"
    discount: float = 0.0

    def _validate_confirmation(self, customer_debt=0):
        #Validacion se hace un metodo externo por REFRACTOR
        if self.status == "CONFIRMED":
            raise ValueError("Already confirmed.")
        if self.total <= 0:
            raise ValueError("total must be positive")
        if customer_debt > 0:
            raise CustomerHasDebt("outstanding debt")

    def confirm(self, customer_debt=0):
        self._validate_confirmation(customer_debt)
        self.discount = round(self.total * 0.15, 2) if self.vip else 0.0
        self.status = "CONFIRMED"
        return self.total - self.discount
