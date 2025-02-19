class InsufficientStockError(Exception):
    """
    Raised when there is not enough stock to fulfill a purchase.
    """

    pass


class InvalidProductError(Exception):
    """
    Raised when an invalid product is used in an order.
    """

    pass
