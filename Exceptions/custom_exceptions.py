class ProductNotFoundException(Exception):
    def __init__(self, product_id):
        self.product_id = product_id
        self.message = f"Product with ID '{product_id}' not found"
        super().__init__(self.message)


class StoreNotFoundException(Exception):
    def __init__(self, store_id):
        self.store_id = store_id
        self.message = f"Store with ID '{store_id}' not found"
        super().__init__(self.message)


class CustomerNotFoundException(Exception):
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.message = f"Customer with ID '{customer_id}' not found"
        super().__init__(self.message)


class InsufficientInventoryException(Exception):
    def __init__(self, product_id, available_quantity, requested_quantity):
        self.product_id = product_id
        self.available_quantity = available_quantity
        self.requested_quantity = requested_quantity

        self.message = (
            f"Insufficient inventory for product '{product_id}'. "
            f"Available: {available_quantity}, "
            f"Requested: {requested_quantity}"
        )

        super().__init__(self.message)


class InvalidSalesException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PipelineException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
