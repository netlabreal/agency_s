import urllib, requests, os
from models import Object
from bs4 import BeautifulSoup



def get_html(url):
    req = requests.get(url)
    return req.text


def read_imgs(nom, dat):
    url = "http://sobstvennik.crmnedv.ru/uploads/resize_images/resize_deault_realty_view_slider_first/7284082365418676823528646a3f979155360.png"

    directory = "media/foto/%s" % (nom, )
    if not os.path.exists(directory):
        os.makedirs(directory)
    cnt = 1
    for k in dat:
        p = requests.get(k)
        print(k)
        out = open("%s/%s.jpg" % (directory, cnt), "wb")
        out.write(p.content)
        out.close()
        cnt = cnt + 1


def get_data_sobstvennik():
    data_links = []

    for k in range(1):
        a = k + 1
        print(a)
        soup = BeautifulSoup(get_html('http://sobstvennik.crmnedv.ru/agency/realty?category_id=7&rent=sale&page=%s' % a), 'html.parser')
        tds = soup.find_all("div", class_="property")
        for j in tds:
            l = j.find_all('a', class_='advertisement__button-more')[1].get("href")
            ol = j.find_all('a', class_='advertisement__button-more')[1].text

            links_img = ""
            l_i = []
            dop_soup = BeautifulSoup(get_html("%s%s" % ("http://sobstvennik.crmnedv.ru", l)), 'html.parser')
            #dop_soup = BeautifulSoup(get_html("http://sobstvennik.crmnedv.ru/agency/realty/view/11249"), 'html.parser')
            map = dop_soup.find("div", class_="view_main")
            latitude = map.find(id="latitude").get("value")
            longitude = map.find(id="longitude").get("value")

            imgs = dop_soup.find("div", class_="slider-preview").find_all("img")
            for i in imgs:
                 links_img += "%s%s," % ("http://sobstvennik.crmnedv.ru", (i.get("src")))
                 l_i.append("%s%s" % ("http://sobstvennik.crmnedv.ru", (i.get("src"))))
            dop_trs = dop_soup.find_all("table", class_="table-striped")
            cost = dop_soup.find('div', class_="price").text
            desc = ""
            d = dop_soup.find('div', class_="offer-description").find("p")
            if d: desc = d.text

            # Parametrs
            city = rayon = street = komn = etag = agent = id = ""
            id = dop_soup.find("span", class_="advertisement-id").text

            agent = dop_soup.find("div", class_="name").text
            trs = dop_trs[0].find_all("tr", class_="category-param-tr")
            for u in range(len(trs)):
                lll = trs[u].find("th").text
                if lll == "Комнат в квартире":
                    komn = trs[u].find("td", class_="overview_td").text
                if lll == "Комнат в квартире":
                    etag = trs[u].find("td", class_="overview_td").text
            trs_dop = dop_trs[1].find_all("tr")
            for u in range(len(trs_dop)):
                lll = trs_dop[u].find("th").text
                if lll == "Населенный пункт":city = trs_dop[u].find("td").text
                if lll == "Район города":rayon = trs_dop[u].find("td").text
                if lll == "Улица":street = trs_dop[u].find("td").text

            data = [desc, id, ("%s%s" % ("http://sobstvennik.crmnedv.ru", l)), ol, city, rayon, street, komn, etag, cost, links_img, str(latitude), str(longitude), agent]
            data_links.append(data)
            print(data)
            read_imgs(id, l_i)


if __name__ == "__main__":
    #get_data_sobstvennik()
    new_object("VASA")