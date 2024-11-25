import requests
import csv
import os

def fetch_data(endpoint):
    data_list = []
    page_number = 1
    page_size = 100  # You can adjust the page size if needed
    total_pages = None

    print(f"Fetching data from {endpoint}...")
    while True:
        params = {
            'page[number]': page_number,
            'page[size]': page_size,
            'format': 'json'
        }
        url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service' + endpoint
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch data from {url} on page {page_number}. Status code: {response.status_code}")
            break

        json_data = response.json()
        data = json_data.get('data', [])
        if not data:
            print("No more data available.")
            break

        data_list.extend(data)

        if total_pages is None:
            meta = json_data.get('meta', {})
            total_pages = meta.get('total-pages', 1)
            print(f"Total pages to fetch: {total_pages}")

        if page_number >= total_pages:
            print("All pages have been fetched.")
            break

        page_number += 1

    return data_list

def save_to_csv(data_list, filename):
    if not data_list:
        print(f"No data to save for {filename}.")
        return

    # Ensure all keys are captured
    keys = set()
    for data in data_list:
        keys.update(data.keys())

    keys = sorted(keys)

    # Create directory if it doesn't exist
    os.makedirs('csv_data', exist_ok=True)
    filepath = os.path.join('csv_data', filename)

    with open(filepath, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_list)

    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    base_url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service'
    endpoints = [
        '/v2/debt/tror/data_act_compliance',
        '/v2/accounting/od/redemption_tables',
        '/v2/accounting/od/title_xii',
        '/v2/accounting/od/avg_interest_rates',
        '/v1/accounting/dts/operating_cash_balance',
        '/v1/accounting/dts/deposits_withdrawals_operating_cash',
        '/v1/accounting/dts/public_debt_transactions',
        '/v1/accounting/dts/adjustment_public_debt_transactions_cash_basis',
        '/v1/accounting/dts/debt_subject_to_limit',
        '/v1/accounting/dts/inter_agency_tax_transfers',
        '/v2/accounting/od/debt_to_penny',
        '/v2/accounting/od/combined_statement',
        '/v2/accounting/od/available_balances',
        '/v2/accounting/od/estimated_financing',
        '/v2/accounting/od/gov_receipts',
        '/v2/accounting/od/gov_outlays',
        '/v2/accounting/od/int_exp',
        '/v2/accounting/od/int_exp_summary',
        '/v2/accounting/od/mspd',
        '/v2/accounting/od/monthly_statement',
        '/v2/accounting/od/pd_schedules',
        '/v2/accounting/od/pd_summary',
        '/v2/accounting/od/tic',
        '/v2/accounting/od/pd_detail',
        # Add more endpoints here as needed
    ]

    for endpoint in endpoints:
        data = fetch_data(endpoint)
        filename = endpoint.strip('/').replace('/', '_') + '.csv'
        save_to_csv(data, filename)
