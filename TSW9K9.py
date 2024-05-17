from abc import ABC
import datetime


class Szoba(ABC):

    def __init__(self, ar, szobaszam, agyakszama):
        self.ar = ar
        self.szobaszam = szobaszam
        self.agyakszama = agyakszama

    def __repr__(self) -> str:
        return "Szoba #{}. {} ágyas. Ár: {}".format(self.szobaszam, self.agyakszama, self.ar)


class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, bovitheto=True):
        super().__init__(ar, szobaszam, 1)
        self.bovitheto = bovitheto


class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, babaagy=False):
        super().__init__(ar, szobaszam, 2)
        self.babaagy = babaagy


class Szalloda:

    def __init__(self, szobak, nev):
        self.szobak = szobak
        self.foglalt_szobak = dict()
        self.nev = nev

    def foglalas(self, foglalas):
        szoba = self.ervenyes_szoba_ellenorzes(foglalas.szoba_szam)

        if self.foglalt_e_a_szoba(foglalas.szoba_szam, foglalas.datum) < 0:
            self.foglalt_szobak[foglalas.datum].append(foglalas.szoba_szam)
            return szoba.ar
        raise ValueError("A szoba már foglalt ezen a napon!")

    def lemondas(self, foglalas):
        self.ervenyes_szoba_ellenorzes(foglalas.szoba_szam)

        foglalas_index = self.foglalt_e_a_szoba(foglalas.szoba_szam, foglalas.datum)
        if foglalas_index >= 0:
            del self.foglalt_szobak[foglalas.datum][foglalas_index]
            return
        raise ValueError("Nincs foglalva ez a szoba ezen a napon!")

    def osszes_foglalas(self):
        return self.foglalt_szobak

    def foglalasok_adott_napon(self, datum):
        foglalt_szobak = []
        if datum not in self.foglalt_szobak:
            self.foglalt_szobak[datum] = foglalt_szobak
        else:
            foglalt_szobak = self.foglalt_szobak[datum]
        return foglalt_szobak

    def szabad_szobak(self, datum):
        foglalt_szobak = self.foglalasok_adott_napon(datum)
        if len(foglalt_szobak) == 0:
            return self.szobak
        szabad_szobak = []
        for szoba in self.szobak:
            for foglalt_szobaszam in foglalt_szobak:
                if szoba.szobaszam == foglalt_szobaszam:
                    break
            else:
                szabad_szobak.append(szoba)

        return szabad_szobak

    def ervenyes_szoba_ellenorzes(self, ellenorizendo_szoba_szobaszam):
        for szoba in self.szobak:
            if szoba.szobaszam == ellenorizendo_szoba_szobaszam:
                return szoba
        raise ValueError("Nincs ilyen szamú szoba!")

    def foglalt_e_a_szoba(self, foglalando_szoba_szam, datum):
        szobafoglalasok = self.foglalasok_adott_napon(datum)
        for index, szoba_szam in enumerate(szobafoglalasok):
            if szoba_szam == foglalando_szoba_szam:
                return index
        return -1


class Foglalas:
    def __init__(self, szoba_szam, datum) -> None:
        self.szoba_szam = szoba_szam
        self.datum = datum


def datum_keres():
    while True:
        datum = input("Adjon meg egy dátumot (ÉÉÉÉ-HH-NN): ")
        try:
            datum = datetime.date.fromisoformat(datum)
            ma = datetime.date.today()
            if datum < ma:
                print("Nem foglalhat múltbéli időpontot!")
            else:
                return datum
        except ValueError:
            print("Érvénytelen dátum!")


def print_foglalhato_szobak(szalloda, datum):
    szabad_szobak = szalloda.szabad_szobak(datum)
    if len(szabad_szobak) == 0:
        print("Nincs foglalható szoba ezen a napon!")
    else:
        print("Foglalható szobák: \n")
        for szoba in szabad_szobak:
            print(szoba)


def print_foglalt_szobak(szalloda, datum):
    foglalt_szobak = szalloda.foglalasok_adott_napon(datum)
    if len(foglalt_szobak) == 0:
        print("Nincs foglalás ezen a napon!")
    else:
        print("Melyik szobát szeretné lemondani?")
        for szoba_szam in foglalt_szobak:
            print("Szoba #", szoba_szam)


def szoba_foglalas(szalloda, datum):
    while True:
        szobaszam = input("Adjon meg egy szoba számot: ")
        try:
            szobaszam = int(szobaszam)
            try:
                return szalloda.foglalas(Foglalas(szobaszam, datum))
            except ValueError as e:
                print(str(e))
        except:
            print("Nem számot adott meg.")


def szoba_lemondas(szalloda, datum):
    while True:
        szobaszam = input("Adjon meg egy szoba számot: ")
        try:
            szobaszam = int(szobaszam)
            try:
                szalloda.lemondas(Foglalas(szobaszam, datum))
                break
            except ValueError as e:
                print(str(e))
        except:
            print("Nem számot adott meg.")


szalloda = Szalloda([
    EgyagyasSzoba(100, 1),
    KetagyasSzoba(180, 2),
    KetagyasSzoba(200, 3, True)
], "Szuper")

szalloda.foglalas(Foglalas(1, datetime.date.today() + datetime.timedelta(days=1)))
szalloda.foglalas(Foglalas(2, datetime.date.today() + datetime.timedelta(days=1)))
szalloda.foglalas(Foglalas(1, datetime.date.today() + datetime.timedelta(days=3)))
szalloda.foglalas(Foglalas(1, datetime.date.today() + datetime.timedelta(days=4)))
szalloda.foglalas(Foglalas(3, datetime.date.today() + datetime.timedelta(days=5)))

print("Üdvözöljük a {} szállodában".format(szalloda.nev))
while True:
    muvelet = input("Vállasszon műveletet:\nf - foglalás\nl - lemondás\nm - foglalások megtekintése\nk - Kilépés\n")
    if muvelet == "f":
        datum = datum_keres()
        print_foglalhato_szobak(szalloda, datum)
        if len(szalloda.szabad_szobak(datum)) > 0:
            foglalas_ara = szoba_foglalas(szalloda, datum)
            print("Sikeres foglalás. A foglalás ára: ", foglalas_ara)
    elif muvelet == "l":
        datum = datum_keres()
        print_foglalt_szobak(szalloda, datum)
        if len(szalloda.foglalasok_adott_napon(datum)) > 0:
            szoba_lemondas(szalloda, datum)
            print("Sikeres lemondás!")
    elif muvelet == "m":
        for datum, szobaszamok in szalloda.osszes_foglalas().items():
            if len(szobaszamok) > 0:
                print("{} napon a kövektkező szobák foglaltak: {}".format(datum, ", ".join(
                    map(lambda s: str(s), szobaszamok))))
    elif muvelet == "k":
        break
    else:
        print("Érvénytelen művelet!")
