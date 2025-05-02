from functools import reduce
from functools import partial
import random

def losuj_karte():
    karty = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Walet', 'Dama', 'Krol', 'As']
    return random.choice(karty)

def wartosc_karty(karta):
    return 10 if karta in ['Walet', 'Dama', 'Krol'] else 11 if karta == 'As' else int(karta)

def policz_punkty(reka):
    punkty = sum(map(wartosc_karty, reka))
    asy = reka.count('As')

    return reduce(lambda p, _ : p - 10 if p > 21 else p, range(asy), punkty)

def wyswietl_reke(gracz, zakryta=False):
    return f"{gracz[0]} [Zakryta]" if zakryta else ' '.join(map(str, gracz))

def pobierz_akcje():
    return input("Czy dobierasz kartę? (t/n): ").lower()

def dodaj_karte_do_reki(reka, talia):
    if not talia:
        print("Talia kart jest pusta. Koniec gry.")
        return reka, False
    reka.append(talia.pop())
    return reka, True

def koniec_gry(gracz, krupier):
    def wyswietl_reke_info(reka):
        return f"{wyswietl_reke(reka)} (Suma: {policz_punkty(reka)})"

    def zwyciezca():
        punkty_krupiera = policz_punkty(krupier)
        punkty_gracza = policz_punkty(gracz)

        if punkty_krupiera > 21 or punkty_gracza > punkty_krupiera:
            return "Gratulacje! Wygrywasz!"
        elif punkty_gracza == punkty_krupiera:
            return "Remis!"
        else:
            return "Przegrywasz! Krupier wygrywa."

    print(f"\nTwoje karty: {wyswietl_reke_info(gracz)}")
    print(f"Karty krupiera: {wyswietl_reke_info(krupier)}\n")
    print(zwyciezca())

def inicjalizuj_gre():
    def utworz_talie():
        talia = [losuj_karte() for _ in range(52)]
        random.shuffle(talia)
        return talia

    def rozdaj_karty(talia):
        gracz = [talia.pop(), talia.pop()]
        krupier = [talia.pop(), talia.pop()]
        return talia, gracz, krupier

    talia = utworz_talie()
    talia, gracz, krupier = rozdaj_karty(talia)

    return talia, gracz, krupier

def wyswietl_stan_gry(gracz, krupier):
    print(f"Twoje karty: {wyswietl_reke(gracz)} (Suma: {policz_punkty(gracz)})")
    print(f"Karta krupiera: {wyswietl_reke(krupier, zakryta=True)}")

def sprawdz_blackjack(gracz):
    def wynik_blackjack(punkty):
        return "Blackjack! Wygrywasz!" if punkty == 21 else ""

    punkty_gracza = policz_punkty(gracz)
    rezultat = wynik_blackjack(punkty_gracza)

    return rezultat

def runda_gracza(gracz, krupier, talia):
    def wykonaj_runde(gracz, krupier, talia):
        def kolejna_runda(gracz, krupier, talia):
            wyswietl_stan_gry(gracz, krupier)

            if sprawdz_blackjack(gracz):
                return True

            akcja = pobierz_akcje()
            if akcja == 't':
                return wykonaj_akcje_gracza(gracz, krupier, talia) and kolejna_runda(gracz, krupier, talia)
            else:
                return True

        return kolejna_runda(gracz, krupier, talia)

    return wykonaj_runde(gracz, krupier, talia)

def wykonaj_akcje_gracza(gracz, krupier, talia):
    def przekroczenie_21(gracz):
        return policz_punkty(gracz) > 21

    def wyswietl_przegrana(gracz):
        print(f"Przekroczyłeś 21! Przegrywasz! Twoje karty: {wyswietl_reke(gracz)}")

    def akcja_po_dobraniu_karty(gracz, talia):
        return dodaj_karte_do_reki(gracz, talia)

    if not akcja_po_dobraniu_karty(gracz, talia):
        return False

    if przekroczenie_21(gracz):
        wyswietl_przegrana(gracz)
        return False

    return True

def runda_krupiera(krupier, talia):
    def wykonaj_runde_krupiera(krupier, talia):
        if policz_punkty(krupier) < 17:
            krupier, _ = dodaj_karte_do_reki(krupier, talia)
            return wykonaj_runde_krupiera(krupier, talia)
        else:
            return krupier

    return wykonaj_runde_krupiera(krupier, talia)

def blackjack():
    talia, gracz, krupier = inicjalizuj_gre()

    while True:
        if not runda_gracza(gracz, krupier, talia):
            break

        runda_krupiera(krupier, talia)
        koniec_gry(gracz, krupier)
        break

def graj_jedna_partie():
    blackjack()

def czy_grac_ponownie():
    return any(map(lambda x: x.lower() == 't', input("Czy chcesz zagrać ponownie? (t/n): ")))

def graj_do_poki_nie_koniec():
    while True:
        graj_jedna_partie()
        if not czy_grac_ponownie():
            print("Dziękujemy za grę! Do zobaczenia!")
            break

graj_do_poki_nie_koniec()

