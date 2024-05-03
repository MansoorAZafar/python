# views.py
from django.utils import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Consumer, ParkingLots, Price, Comments, Reservations

@csrf_exempt
def add_comment(request) -> JsonResponse:
    """
    * Adds a comment assoicated with a specific Slot into the database. 

    Parameters:
    ------------
    * request
        - The HTTP request being sent (Need to send a POST request to add any information)
            - the body should include 2 values: 'comment' and 'slot_id'
                
            * comment : str
                - The content of the 'comment' to be assoicated with a Slot
            * slot_id : int
                - the slot that will be marked as booked and associated with the Reservation
    """

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment = data['comment']
            slot_id = data['slot_id']
            parking_lot = ParkingLots.objects.get(pk=slot_id)
            comment_obj = Comments.objects.create(description=comment, Slot_ID=parking_lot)
            return JsonResponse({'message': 'Comment added successfully'}, status=200)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except ParkingLots.DoesNotExist:
            return JsonResponse({'error': 'Slot not found'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_comments(request) -> JsonResponse:
    """
    * Grabs all comments assoicated from a specific Slot into the database. 
    
    Parameters:
    ------------
        * request
            - The HTTP request being sent (Need to send a GET request to get any information)
                - the url should include the query parameter of 'slot_id'
                ex. /get_comments/?slot_id=[value]
                    
            * slot_id
                - the slot that will be marked as booked and associated with the Reservation
    """

    if request.method == 'GET':
        slot_id = request.GET.get('slot_id')
        try:
            comments = Comments.objects.filter(Slot_ID=slot_id).values()
            return JsonResponse(list(comments), safe=False)
        except Exception as e:
            return JsonResponse({'error': 'could not get comment'}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_available_locations(request) -> JsonResponse:
    """
    * Grabs all the free parking spaces that aren't reserved and are the type 'condition'
    
    Parameters:
    ------------
        * request
            - The HTTP request being sent (Need to send a GET request to get any information)
                - the url should include the query parameter of 'condition'
                ex. /get_available_locations/?condition=[value]
                    
            * condition
                - The type of parking space to be returned
                - By default, is set to all types of parking spaces
    """

    if request.method == 'GET':
        condition = request.GET.get('condition', 'all')
        try:
            cleanup_expired_reservations();
            available_locations = ParkingLots.db_get_available_locations(condition)
            return JsonResponse({'available_locations': list(available_locations.values())}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def cleanup_expired_reservations():
    """
    * Clears out all the reservations in the Reservation table that's expiry had already passed
    """
    # Get current time
    current_time = timezone.now()
    # Filter expired reservations
    expired_reservations = Reservations.objects.filter(expiry__lte=current_time)
    
    # Update corresponding ParkingLots to mark slots as unbooked
    for reservation in expired_reservations:
        parking_lot = reservation.Slot_ID
        parking_lot.booked = False
        parking_lot.save()
    
    # Delete expired reservations
    expired_reservations.delete()


def slot_type(request) -> JsonResponse:
    """
    * Returns the type of a Slot ("inner" or "outer") from a given Slot
    
    Parameters:
    ------------
        * request
            - The HTTP request being sent (Need to send a GET request to get any information)
                - the url should include the query parameter of 'slot_id'
                ex. /slot_type/?slot_id=[value]
                    
            * slotID : int
                - The specific slot to find which type it is
    """

    if request.method == 'GET':
        slot_id = request.GET.get('slot_id')
        try:
            type_of_slot = ParkingLots.get_type_of(slot_id)
            if type_of_slot: return JsonResponse({'slot type is ': type_of_slot})
            else: return JsonResponse({"error": "slot does not exist"}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def authenticate_user(request) -> JsonResponse:
    """
    * Checks if the entered username and password exist in the Datbase. 
    * Return 403 {}"error": "Invalid Credentials"} if no such user exists or bad credentials
    
    Parameters:
    ------------
        * request
            - The HTTP request being sent (Need to send a GET request to get any information)
                - the url should include the query parameter of 'username' and 'password'
                ex. /slot_type/?username=[value]&password=[value]
                    
            * username
                - The username of the user
            * password
                - the password of the respective user
    """

    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = Consumer.objects.filter(username=username, password=password).values()
            if user:
                return JsonResponse({'success': True, 'user': list(user)[0]})
            else:
                return JsonResponse({"error":"Invalid Credentials"}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def add_user(request) -> JsonResponse:
    """
    * Adds a new user into the Consumer table 
    
    Parameters:
    ------------
        * request
            - The HTTP request being sent (Need to send a POST request to add any information)
                - the body should include 'username' and 'password'
                    
            * username
                - The username of the user
            * password
                - the password of the respective user
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        if Consumer.get_user(username):
            return JsonResponse({'error': 'User already Exists'}, status=403)
        user = Consumer.objects.create(username=username, password=password)
        return JsonResponse({'message': 'User added successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def remove_reservation(request) -> JsonResponse:
    """
    * removes a reservation for a specific Slot from the Reservation table

    Parameters:
    ------------
    * request
        - The HTTP request being sent (Need to send a DELETE request to remove any information)
            - the body should include the 'slot_id' 
            
            * slot_id : int
                - The slot being removed from the reservation 
    """

    if request.method == 'DELETE':
        data = json.loads(request.body)
        slot_id = data['slot_id']
        try:
            # Call the db_remove_reservation function from ParkingLots model
            removed = ParkingLots.db_remove_reservation(slot_id)
            if removed: return JsonResponse({'message': 'Reservation removed successfully'})
            else: return JsonResponse({'error':'No such Reservation'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_your_reservations(request) -> JsonResponse:
    """
    * Returns a JSON list of all the reservations associated to a user

    Parameters:
    ------------
    * request
        - The HTTP request being sent (Need to send a GET request to get any information)
            - the url should include the query parameter of username
            ex. /get_your_reservations/?username=[value]
            
            * username : str
                - the user that will actually be added to the Reservation table
    """

    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            # Call the db_get_your_reservations function from Reservations model
            reservations = Reservations.db_get_your_reservations(username)
            return JsonResponse({'reservations': reservations})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

#Ensures you don't need a crsf key in your header
@csrf_exempt
def add_reservation(request) -> JsonResponse:
    """
    * Adds a reservation for a specific user to the Reservations table from the Database

    Parameters:
    ------------
    * request
        - The HTTP request being sent (Need to send a POST request to add any information)
            - the body should include 3 values: 'username', 'slot_id' and 'expiry_hours'
                * username : str
                        - the user that will actually be added to the Reservation table
                * slot_id : int
                    - the slot that will be marked as booked and associated with the Reservation
                * expiry_hours : int   
                    - the amount of time the user will have reserved in hours
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        slot_id = data['slot_id']
        expiry_hours = data['expiry_hours']
        try:
            # Call the db_add_reservation function from Reservations model
            Reservations.db_add_reservation(username, slot_id, expiry_hours)
            return JsonResponse({'message': 'Reservation added successfully'})
        except Exception as e:
            return JsonResponse({'error': 'Slot is already booked'}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    


def add_default_data(request):
    """
    * This function is used to initalize default values for the database 

    Parameters:
    ------------
    * request
        - The HTTP request being sent (it can be any)
    """

    try:
        # Initialize default values for parking lots
        for _ in range(1, 20 + 1):
            ParkingLots.objects.create(type='inner')

        for _ in range(1, 30 + 1):
            ParkingLots.objects.create(type='outer')

        # Initialize default values for prices
        Price.objects.create(type='inner', cost=20.25, hourly_increase=2.35)
        Price.objects.create(type='outer', cost=30.19, hourly_increase=4.32)

        return JsonResponse({'message': 'Default values initialized successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)})