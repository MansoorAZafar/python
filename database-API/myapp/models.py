# models.py
from django.db import models
from datetime import timedelta
from django.utils import timezone

class Consumer(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    @staticmethod
    def get_user(username: str):
        """
        * Ensures two users with the same username cannot exist

        Parameters:
        ------------
        * username : str
            - the username that will be registered
        """
        return Consumer.objects.filter(username=username)

class ParkingLots(models.Model):
    TYPE_CHOICES = [('inner', 'Inner'), ('outer', 'Outer')]
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    booked = models.BooleanField(default=False)

    @staticmethod
    def db_get_available_locations(condition: str="all"):
        """
        * Grabs all the free parking spaces that aren't reserved and are the type 'condition'

        Parameters:
        ------------
        * condition : str
            - The type of parking space to be returned
            - By default, is set to all types of parking spaces
        """

        if condition.lower() == "inner":
            return ParkingLots.objects.filter(type="inner", booked=False)
        elif condition.lower() == "outer":
            return ParkingLots.objects.filter(type="outer", booked=False)
        else:
            return ParkingLots.objects.filter(booked=False)
        
    @staticmethod 
    def get_type_of(slotID: int) -> str:
        """
        * Returns the type of a Slot ("inner" or "outer") from a given Slot

        Parameters:
        ------------
        * slotID : int
            - The specific slot to find which type it is
        """

        try:
            slot = ParkingLots.objects.get(pk=slotID)
            return slot.type
        except ParkingLots.DoesNotExist:
            return None

    @staticmethod
    def db_remove_reservation(Slot_ID: int) -> bool:
        """
        * removes a reservation for a specific Slot from the Reservation table

        Parameters:
        ------------
        * Slot_ID : int
            - The slot being removed from the reservation 
        """

        try:
            reservation = Reservations.objects.get(Slot_ID=Slot_ID)
            reservation.delete()
            # Update ParkingLots to mark the slot as not booked
            parking_lot = ParkingLots.objects.get(pk=Slot_ID)
            parking_lot.booked = False
            parking_lot.save()
            return True
        except Reservations.DoesNotExist:
            return False;

class Comments(models.Model):
    description = models.CharField(max_length=250)
    Slot_ID = models.ForeignKey(ParkingLots, on_delete=models.CASCADE)

class Price(models.Model):
    type = models.CharField(max_length=10, primary_key=True)
    cost = models.FloatField()
    hourly_increase = models.FloatField()

class Reservations(models.Model):
    price = models.FloatField()
    expiry = models.DateTimeField()
    Slot_ID = models.ForeignKey(ParkingLots, on_delete=models.CASCADE)
    userID = models.ForeignKey(Consumer, on_delete=models.CASCADE)

    @staticmethod
    def db_get_your_reservations(username: str) -> list:
        """
        * Returns a list of all the reservations associated to a user

        Parameters:
        ------------
        * condition : str
            - The type of parking space to be returned
            - By default, is set to all types of parking spaces
        """

        try:
            user = Consumer.objects.get(username=username)
            reservations = Reservations.objects.filter(userID=user).values()
            return list(reservations)
        except Consumer.DoesNotExist:
            return []

    @staticmethod
    def db_add_reservation(username: str, 
                           slot_id: int, 
                           expiry_hours: float) -> None:
        """
        * MAY RAISE AN EXCEPTION 
        * (Use with try & Except)
        * Adds a reservation for a specific user to the Reservations table from the Database

        Parameters:
        ------------
        * username : str
            - the user that will actually be added to the Reservation table
        * slot_id : int
            - the slot that will be marked as booked and associated with the Reservation
        * expiry_hours : float 
            - the amount of time the user will have reserved in hours
        """

        try:
            parking_lot = ParkingLots.objects.get(pk=slot_id)
            if parking_lot.booked:
                raise Exception("Slot is already booked")
            price_info = Price.objects.filter(type=parking_lot.type).values('hourly_increase').first()
            if price_info:
                hourly_increase = price_info['hourly_increase']
                initial_price = hourly_increase * expiry_hours
                user = Consumer.objects.get(username=username)
                expiry_time = timezone.now() + timezone.timedelta(hours=expiry_hours)
                reservation = Reservations.objects.create(price=initial_price, expiry=expiry_time, Slot_ID=parking_lot, userID=user)
                # Update ParkingLots to mark the slot as booked
                parking_lot.booked = True
                parking_lot.save()
            else:
                raise Exception("Slot type not found in Price table")
        except ParkingLots.DoesNotExist:
            raise Exception("Slot not found")
