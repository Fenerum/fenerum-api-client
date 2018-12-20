from urllib.parse import urljoin  # python2: from urlparse import urljoin
import requests
from fenerum.exceptions import FenerumConnectionError, FenerumNotFoundError, FenerumCriticalError, FenerumValidationError


class FenerumClient:

    def __init__(self, api_token):
        self.api_token = api_token

    def make_request(self, relative_url, method='get', data=None, **kwargs):
        try:
            r = requests.request(
                method=method,
                url=urljoin('https://app.fenerum.com/api/v1/', relative_url),
                json=data,
                headers={
                    'Authorization': 'Token %s' % self.api_token,
                },
                timeout=10,
                **kwargs
            )
        except (requests.ConnectionError, requests.Timeout) as e:
            raise FenerumConnectionError(e.response)

        if r.status_code == 404:
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                raise FenerumNotFoundError(e.response)
        elif r.status_code >= 500:
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                raise FenerumCriticalError(e.response)
        else:
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                raise FenerumValidationError(r.json())

        return r.json()

    def get_account(self, account_code):
        return self.make_request('accounts/{}/'.format(account_code))

    def create_account(self, account_code, company_name, legal_address, legal_zipcode, legal_city, legal_country, legal_vat_number=None):
        return self.make_request('accounts/', method='post', data={
            'code': account_code,
            'company_name': company_name,
            'legal_address': legal_address,
            'legal_zipcode': legal_zipcode,
            'legal_city': legal_city,
            'legal_country': legal_country,
            'legal_vat_number': legal_vat_number,
        })

    def update_account(self, account_code, company_name, legal_address, legal_zipcode, legal_city, legal_country, legal_vat_number=None):
        return self.make_request('accounts/{}/'.format(account_code), method='put', data={
            'code': account_code,
            'company_name': company_name,
            'legal_address': legal_address,
            'legal_zipcode': legal_zipcode,
            'legal_city': legal_city,
            'legal_country': legal_country,
            'legal_vat_number': legal_vat_number,
        })

    def create_subscription(self, account_code, terms_uuid, quantity, collection_method):
        return self.make_request('accounts/{}/subscribe/'.format(account_code), method='post', data={
            'terms': terms_uuid,
            'quantity': quantity,
            'collection_method': collection_method,
        })

    def create_recipient(self, name, email, receive_invoice=True, receive_payment_confirmation=True, receive_subscription_notifications=True):
        return self.make_request('recipients/', method='post', data={
            'name': name,
            'email': email,
            'receive_invoice': receive_invoice,
            'receive_payment_confirmation': receive_payment_confirmation,
            'receive_subscription_notifications': receive_subscription_notifications,
        })

    def create_payment_card(self, account_uuid, stripe_token):
        return self.make_request('paymentcards/', method='post', data={
            'account': account_uuid,
            'gateway': 'stripe',
            'token': stripe_token,
        })

    def disable_payment_card(self, payment_card_uuid):
        return self.make_request('paymentcards/{}/disable/'.format(payment_card_uuid), method='post', data={})

    def get_plans(self):
        return self.make_request('plans/')

    def calculate_plan_price(self, account_country_code, terms, quantity, account_code=None):
        return self.make_request('plans/calculate/', method='post', data={
            'account_code': account_code,
            'account_country_code': account_country_code,
            'terms': terms,
            'quantity': quantity,
        })
