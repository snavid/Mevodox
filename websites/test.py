import requests
from bs4 import BeautifulSoup

def get_members_information(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    members = []

    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        photo_url = cells[0].find('img')['src']
        first_name = cells[1].text.strip()
        middle_name = cells[2].text.strip()
        surname = cells[3].text.strip()
        constituent = cells[4].text.strip()
        party = cells[5].text.strip()
        member_type = cells[6].text.strip()

        member_data = {
            'photo_url': photo_url,
            'first_name': first_name,
            'middle_name': middle_name,
            'surname': surname,
            'constituent': constituent,
            'party': party,
            'member_type': member_type,
        }
        members.append(member_data)

    return members

if __name__ == "__main__":
    url = "https://www.parliament.go.tz/mps-list"  # Replace with the URL containing the HTML table
    members_info = get_members_information(url)
    for member in members_info:
        print(member)