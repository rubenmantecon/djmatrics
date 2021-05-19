from core.models import *
import datetime


def calculatePrice(matricula: Enrolment):
    PUBLIC_PRICE = 360
    UF_PRICE
    MATERIAL = 70
    insurance = 1.12

    ufs_prices = matricula.uf.all().count() *

    age = int((datetime.date.today() -
              matricula.birthday).total_seconds() / 31557600)

    if age > 28:
        insurance = 20

    if ufs_prices > PUBLIC_PRICE:
        final_price = public_price + material + insurance
        return final_price
    else:
        final_price = ufs_prices + material + insurance
        return final_price

matricula = Enrolment.objects.first()
calculatePrice(matricula)
