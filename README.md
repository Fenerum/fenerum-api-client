# Fenerum API Client

Please note, this is a very early version of the future Fenerum API Client. Use at own risk!


### Example usage

```python
from fenerum import FenerumClient, FenerumError

fenerum_client = FenerumClient(MY_SECRET_TOKEN)

try:
    fenerum_client.create_account(
        account_code='5552834000',
        company_name='ACME Inc.',
        legal_address='Street 1B',
        legal_zipcode='B-1000',
        legal_city='Aarhus',
        legal_country='Denmark',
    )
except FenerumError as e:
    # TODO: handle the exception
    pass

```
