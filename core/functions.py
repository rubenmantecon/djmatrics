from core.models import *
import datetime

public_price = 360
material = 70
assurance = 1.12

enrolment = Enrolment.objects.get(dni='12345678Z')
ufs_of_enrolment = UF.objects.filter(
    term=Enrolment.objects.get(dni='12345678Z').term)
ufs_prices = sum([x.price for x in ufs_of_enrolment])
birthday = enrolment.birthday
age = datetime.datetime.now()
if age > 28:
    assurance = 20

if ufs_prices > public_price:
    final_price = public_price + material + assurance
else:
    final_price = ufs_prices + material + assurance
print(ufs_prices)
