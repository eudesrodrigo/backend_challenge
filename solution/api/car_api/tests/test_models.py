from django.test import TestCase
from car_api.models import Car, Tyre, MAX_CAR_TYRES

# models test
class CarTest(TestCase):

    def test_create_tyre(self):
        car_id = Car.create_car()["car_id"]
        car = Car.objects.filter(id=car_id).first()
        car_status_after_trip = Car.trip(car=car, distance=400)
        print(car_status_after_trip)

        tyre_count = Tyre.objects.filter(fk_car_id=car.id).count()
        self.assertEqual(tyre_count, MAX_CAR_TYRES)