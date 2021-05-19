from core.models import *
import datetime


def calculatePrice(id_param):
    # TODO: change id_param to request, and make the query like so: Enrolment.objects.get(id=request.user.id)
    matricula = Enrolment.objects.get(id=id_param)
    public_price = 360
    UF_PRICE = 25
    MATERIAL = 70
    insurance = 1.12
    bonus = 1

    try:
        discount_type = matricula.profile_req.profile_type

        if discount_type == 'MA' or discount_type is None:
            bonus = 1
        elif discount_type == 'BO':
            bonus = 0.5
        elif discount_type == 'EX':
            bonus = 0
    except ProfileRequirement.DoesNotExist:
        print("ProfileRequirement.DoesNotExist: No profile requirement seems to exists in the DB")
        return -1
    except AttributeError:
        print("AttributeError: No profile requirement seems to exists in the DB")
        return -1
    ufs_prices = (matricula.uf.all().count()) * UF_PRICE
    age = int((datetime.date.today() -
              matricula.birthday).total_seconds() / 31557600)

    if age > 28:
        insurance = 20

    if ufs_prices > public_price:
        final_price = public_price * bonus + MATERIAL + insurance
        print(final_price)
    else:
        final_price = ufs_prices * bonus + MATERIAL + insurance
        print(final_price)


# calculatePrice(1)
