from lxml import html
from requests import session
from Pack1.Litmus.utils import cutter
from Pack1.Litmus.utils import deco


def get_items():
    username = input("Your username to Litmus : ").strip()
    while not username:
        username = input("Your username to Litmus : ").strip()
    password = input("Your password to Litmus : ").strip()
    while not password:
        password = input("Your password to Litmus : ").strip()
    clients_url = 'https://litmus.com/'
    how_many = int(input('How many emails do u want? '))

    with session() as c:
        q = c.get(clients_url + 'sessions/new')
        tree = html.fromstring(q.text)
        authenticity_token = tree.xpath('//form[@id=\'login-form\']//input[@name=\'authenticity_token\']')
        payload = {
                'email': username,
                'password': password,
                'authenticity_token': authenticity_token[0].value,
                'remember_me': '1'
                }
        login = c.post(clients_url + 'sessions', data=payload)
        redirected_to = login.url
        if 'new?email=' in redirected_to:
            print('Not logged in')
            return
        else:
            deco(2)
            print('\n Take a deep breath \n And relax \n This may take a while')
            checklists = c.get(clients_url + 'checklist')
            tree = html.fromstring(checklists.text)
            tests = tree.xpath('//a[@class=\'row-item-title\']')

            for i in tests[0: how_many]:
                images = []
                item = c.get(clients_url + i.get("href"))
                tree = html.fromstring(item.text)
                test_name = tree.xpath('//span[@id=\'header-title\']')[0].text.strip()
                links = tree.xpath('//div[@class=\'screenshot\']//img[@class=\'preview-result-img\']')
                deco(2)
                for i in links:
                    img_link = i.get("data-qa-url")
                    redirect_url = c.get('https:' + img_link)
                    valid_url = redirect_url.url
                    images.append(cutter(valid_url))
                    deco(2)
                print('Take a deep breath')
                yield test_name, images

