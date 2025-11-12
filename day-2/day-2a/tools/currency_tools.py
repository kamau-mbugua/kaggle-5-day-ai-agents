"""
Currency Conversion Tools
Custom function tools following ADK best practices:
- Dictionary returns with status
- Clear docstrings
- Type hints
- Error handling
"""


def get_fee_for_payment_method(method: str) -> dict:
    """Looks up the transaction fee percentage for a given payment method.

    This tool simulates looking up a company's internal fee structure based on
    the name of the payment method provided by the user.

    Args:
        method: The name of the payment method. It should be descriptive,
                e.g., "platinum credit card" or "bank transfer".

    Returns:
        Dictionary with status and fee information.
        Success: {"status": "success", "fee_percentage": 0.02}
        Error: {"status": "error", "error_message": "Payment method not found"}
    """
    # This simulates looking up a company's internal fee structure.
    fee_database = {
        "platinum credit card": 0.02,  # 2%
        "gold debit card": 0.035,  # 3.5%
        "bank transfer": 0.01,  # 1%
        "silver card": 0.025,  # 2.5%
        "wire transfer": 0.015,  # 1.5%
    }

    fee = fee_database.get(method.lower())
    if fee is not None:
        return {"status": "success", "fee_percentage": fee}
    else:
        return {
            "status": "error",
            "error_message": f"Payment method '{method}' not found in our system",
        }


def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Looks up and returns the exchange rate between two currencies.

    Args:
        base_currency: The ISO 4217 currency code of the currency you
                       are converting from (e.g., "USD").
        target_currency: The ISO 4217 currency code of the currency you
                         are converting to (e.g., "EUR").

    Returns:
        Dictionary with status and rate information.
        Success: {"status": "success", "rate": 0.93}
        Error: {"status": "error", "error_message": "Unsupported currency pair"}
    """

    # Static data simulating a live exchange rate API
    # In production, this would call: requests.get("api.exchangerates.com")
    rate_database = {
        "usd": {
            "eur": 0.93,  # Euro
            "jpy": 157.50,  # Japanese Yen
            "inr": 83.58,  # Indian Rupee
            "gbp": 0.79,  # British Pound
            "cad": 1.35,  # Canadian Dollar
        },
        "eur": {
            "usd": 1.08,  # US Dollar
            "gbp": 0.85,  # British Pound
            "jpy": 169.50,  # Japanese Yen
        }
    }

    # Input validation and processing
    base = base_currency.lower()
    target = target_currency.lower()

    # Return structured result with status
    rate = rate_database.get(base, {}).get(target)
    if rate is not None:
        return {"status": "success", "rate": rate}
    else:
        return {
            "status": "error",
            "error_message": f"Unsupported currency pair: {base_currency}/{target_currency}",
        }


# Test functions if run directly
if __name__ == "__main__":
    print("Testing Currency Tools")
    print("="*50)

    # Test fee lookup
    print("\n1. Testing fee lookup:")
    print(f"Platinum Credit Card: {get_fee_for_payment_method('platinum credit card')}")
    print(f"Unknown Method: {get_fee_for_payment_method('unknown method')}")

    # Test exchange rate
    print("\n2. Testing exchange rate:")
    print(f"USD to EUR: {get_exchange_rate('USD', 'EUR')}")
    print(f"USD to XYZ: {get_exchange_rate('USD', 'XYZ')}")
