class OrderService:
    def __init__(self, gateway):
        self.gateway = gateway

    def checkout(self, order):
        amount = order.total - round(order.total * 0.15, 2) if order.vip else order.total
        if not self.gateway.charge(amount):
            order.status = "REJECTED"
            raise RuntimeError("payment rejected")
        order.confirm()
        return amount
