from django.core.management.base import BaseCommand, CommandError
from main.models import Object as Obj
from main.models import Agent as Ag
from main.models import Types, Typ, Rayon


import os, requests
from bs4 import BeautifulSoup
from decimal import Decimal


class Command(BaseCommand):
    help = 'Get data from Sobstvennik site'

    def get_html(self, url):
        req = requests.get(url)
        return req.text

    def read_imgs(self, nom, dat):
        directory = "media/foto/%s" % (nom,)
        if not os.path.exists(directory):
            os.makedirs(directory)
        cnt = 1
        for k in dat:
            p = requests.get(k)
            #print(k)
            out = open("%s/%s.jpg" % (directory, cnt), "wb")
            out.write(p.content)
            out.close()
            cnt = cnt + 1

    def get_data_sobstvennik(self):
        data_links = []

        for k in range(10):
            a = k + 1
            print(a)
            soup = BeautifulSoup(
                self.get_html('http://sobstvennik.crmnedv.ru/agency/realty?category_id=7&rent=sale&page=%s' % a),
                'html.parser')
            tds = soup.find_all("div", class_="property")
            for j in tds:
                l = j.find_all('a', class_='advertisement__button-more')[1].get("href")
                ol = j.find_all('a', class_='advertisement__button-more')[1].text
                etag = etags = plosh = 0
                loc = ""
                loc = j.find(class_="location").text
                d_dt = j.find_all('div', class_="area")
                for d in d_dt:
                    rez = d.find('span', class_="key")
                    if rez:
                        if "Площадь:" in rez.text:
                            plosh = d.find('span', class_="value").text[:-3]
                        if "Этаж/Этажность" in rez.text:
                            etag, etags = d.find('span', class_="value").text.split("/")

                links_img = ""
                l_i = []
                dop_soup = BeautifulSoup(self.get_html("%s%s" % ("http://sobstvennik.crmnedv.ru", l)), 'html.parser')
                map = dop_soup.find("div", class_="view_main")
                latitude = map.find(id="latitude").get("value")
                longitude = map.find(id="longitude").get("value")

                imgs = dop_soup.find("div", class_="slider-preview").find_all("img")
                for i in imgs:
                    links_img += "%s%s," % ("http://sobstvennik.crmnedv.ru", (i.get("src")))
                    l_i.append("%s%s" % ("http://sobstvennik.crmnedv.ru", (i.get("src"))))
                dop_trs = dop_soup.find_all("table", class_="table-striped")
                cost = dop_soup.find('div', class_="price").text
                #adr = dop_soup.find('div', class_="location").text

                desc = ""
                d = dop_soup.find('div', class_="offer-description").find("p")
                if d: desc = d.text

                # Parametrs
                city = rayon = street = komn = agent = id = ""
                id = dop_soup.find("span", class_="advertisement-id").text

                agent = dop_soup.find("div", class_="name").text
                trs = dop_trs[0].find_all("tr", class_="category-param-tr")
                for u in range(len(trs)):
                    lll = trs[u].find("th").text
                    if lll == "Комнат в квартире":
                        komn = trs[u].find("td", class_="overview_td").text
                    #if lll == "Этаж":
                    #    etag = trs[u].find("td", class_="overview_td").text
                trs_dop = dop_trs[1].find_all("tr")
                for u in range(len(trs_dop)):
                    lll = trs_dop[u].find("th").text
                    if lll == "Населенный пункт": city = trs_dop[u].find("td").text
                    if lll == "Район города": rayon = trs_dop[u].find("td").text
                    if lll == "Улица": street = trs_dop[u].find("td").text

                data = [desc, id, ("%s%s" % ("http://sobstvennik.crmnedv.ru", l)), ol, city, rayon, street, komn, etag,
                        cost, links_img, str(latitude), str(longitude), agent]
                data_links.append(data)
                #print(data)
                try:
                    o = Obj()
                    o.name = ol
                    o.s = plosh
                    o.s_number = id

                    o.s_ssilka = ("%s%s" % ("http://sobstvennik.crmnedv.ru", l))
                    o.cost = Decimal(cost.replace(' ', ''))
                    #o.adres = "%s %s" % (city, street)
                    o.adres = loc
                    if komn == "Гостинка" or komn == "":
                        o.komnat = 1
                    else:
                        try:
                            o.komnat = komn
                        except Exception as e:
                            o.komnat = 1

                    if etag == "":
                        o.floor = 1
                    else:
                        o.floor = etag
                    if etags == "":
                        o.floors = 1
                    else:
                        o.floors = etags

                    o.mainimage = "1.jpg"
                    o.opisanie = desc

                    a, created = Ag.objects.get_or_create(name=agent)
                    t, created = Types.objects.get_or_create(name="Продажа")
                    tt, created = Typ.objects.get_or_create(name="Квартира")
                    if rayon !='':
                        r, created = Rayon.objects.get_or_create(name=rayon)
                        o.rayon = r
                    o.typ = tt
                    o.type = t
                    o.agent = a
                    if str(latitude) != '': o.shirota = Decimal(str(latitude))
                    if str(longitude) != '': o.dolgota = Decimal(str(longitude))


                    o.save()
                    print(o.s+" - "+o.adres+" - "+str(o.floor)+"/"+str(o.floors))
                    self.read_imgs(o.id, l_i)
                except Exception as e:
                    print(e)
                    print("%s - %s" % (ol, id, ))

    def handle(self, *args, **options):
        #o = Obj()
        #o.name = "VASA"
        #o.komnat = 10
        #o.save()
        self.get_data_sobstvennik()
        print("REAL!!!%s" % "NNNNNNNNNNNNNNNN")
