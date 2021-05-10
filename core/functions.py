from core.models import *
import datetime

public_price = 360
material = 70
insurance = 1.12

enrolment = Enrolment.objects.get(dni='12345678Z')
ufs_of_enrolment = UF.objects.filter(
    term=enrolment.term)
ufs_prices = sum([x.price for x in ufs_of_enrolment])

age = int((datetime.date.today() - enrolment.birthday).total_seconds() / 31557600)


if age > 28:
    insurance = 20

if ufs_prices > public_price:
    final_price = public_price + material + insurance
else:
    final_price = ufs_prices + material + insurance
print("Calculated age:", age)
print("Calculated price:", final_price)
