from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

CAR_MAX_FUEL = 50
KM_PER_LITRE = 8
MAX_CAR_TYRES = 4
MIN_GAS_COUNT_BEFORE_REFUEL = 0.05
MIN_TYRE_DEG_BEFORE_CHANGE = 0.94
TYRES_DEG_CREATE_LIMIT = 0.95
TYRE_DEG_PER_KM = 0.01/3

class Car(models.Model):
    id = models.BigAutoField(primary_key=True)
    total_gas_capacity = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(CAR_MAX_FUEL)], default=CAR_MAX_FUEL)
    gas_count = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=1)

    def trip(car, distance):
        traveled_distance = 0
        for traveled_distance in range (1, distance + 1):
            print(f"Traveled distance: {traveled_distance} Km")

            # Update gas_count for each Km
            car.gas_count -= (1/KM_PER_LITRE)/car.total_gas_capacity
            if car.gas_count < 0:
                car.gas_count = 0
            
            # Refuel if less then MIN_GAS_COUNT_BEFORE_REFUEL
            if car.gas_count <= MIN_GAS_COUNT_BEFORE_REFUEL:
                gas_quantity = (1-car.gas_count) * car.total_gas_capacity
                Car.refuel(car=car, gas_quantity=gas_quantity)

            # Degrade tyres
            tyres = Tyre.objects.filter(fk_car_id=car, degradation__lte=1).all()

            tire_degradated_more_95_counter = 0
            for i, tyre in enumerate(tyres):
                tyre.degradation += TYRE_DEG_PER_KM
                print(f"Tyre {i} degradation: {tyre.degradation * 100} %")
                tyre.save()
                
                if tyre.degradation >= TYRES_DEG_CREATE_LIMIT:
                    tire_degradated_more_95_counter += 1
            
                # Change tires when reach MIN_TYRE_DEG_BEFORE_CHANGE
                if tyre.degradation >= MIN_TYRE_DEG_BEFORE_CHANGE:
                    print("Swapping tyres")
                    new_tyre = Car.create_tyre(car=car)
                    if new_tyre is not None:
                        tyre.delete()

            print(f"Current gas_count: {car.gas_count * 100} %")
            print("*"*50)

        car_status = Car.get_car_status(car.id)
        return car_status

    
    def refuel(car, gas_quantity):
        total_refuel = car.total_gas_capacity*car.gas_count + gas_quantity

        if (total_refuel <= car.total_gas_capacity):
            car.gas_count = total_refuel/car.total_gas_capacity
        else:
            car.gas_count = 1
        car.save()
        print(f"Car refueled with {gas_quantity} litres.")
        return car.gas_count

    
    def maintenance(car_id, part):
        print("Travel")

    def create_car():
        car = Car.objects.create()
        for tyre in range(0, MAX_CAR_TYRES):
            Car.create_tyre(car=car)

        return Car.get_car_status(car.id)

    def get_car_status(car_id):
        car = Car.objects.filter(id=car_id).first()
        tyres = Tyre.objects.filter(fk_car_id=car, degradation__lte=TYRES_DEG_CREATE_LIMIT)
        dict_car_status = {"car_id": car.id, 
                           "car_gas_count": car.gas_count,
                           "tyres_status": [tyre.degradation for tyre in tyres]}

        return dict_car_status

    def create_tyre(car):

        # A tyre should NOT be created while there is 4 usable tyres with less than 95% degradation
        tyre_count = Tyre.objects.filter(fk_car_id=car, degradation__lte=TYRES_DEG_CREATE_LIMIT).count()
        if tyre_count < MAX_CAR_TYRES:
            return Tyre.objects.create(fk_car_id = car)
        else:
            print("You can not create a new tyre because your car has 4 tyres in good conditions.")
            return None

    def __str__(self):
        return self.id


class Tyre(models.Model):
    id = models.BigAutoField(primary_key=True)
    degradation = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=0)
    fk_car_id = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.id
