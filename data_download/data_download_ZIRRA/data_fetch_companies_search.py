import requests

url = "https://zirra.p.rapidapi.com/v1/companies"

querystring = {"ticker":"AAL"}

headers = {
    'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e",
    'x-rapidapi-host': "zirra.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)