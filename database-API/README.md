**Purpose?** <br/>
To read and write information to the simulated Parking Lot Database
------------------------------------------------------
------------------------------------------------------

How to use?
------------------------------------------------------
------------------------------------------------------
Add Comment
------------
method: POST
url: https://database-api-latest.onrender.com/myapp/add_comment/
body: {
	"comment": "text",
	"slot_id": 1
}

Successful output:
{'message': 'Comment added successfully'}

Bad output:
{'error': 'Invalid request method'}


------------------------------------------------------
------------------------------------------------------
Get Comments
------------
method: GET
url: https://database-api-latest.onrender.com/myapp/get_comments/?slot_id=[number]


Successful output:
[
  {
    "id": 1,
    "description": "Hello World! This is for slot 1",
    "Slot_ID_id": 1
  }
]

Bad output:
[]


------------------------------------------------------
------------------------------------------------------
Get Available Locations
------------
method: GET 
url: https://database-api-latest.onrender.com/myapp/get_available_locations/?condition=[type of condition]
types of conditions: all (default), inner, outer 
(if you just do the url without ?condition= it defaults to all)

Successful output:
{
  "available_locations": [
	{
	  "id": 1,
	  "type": "inner",
	  "booked": false
	},
	{
	  "id": 2,
	  "type": "inner",
	  "booked": false
	},...
}


------------------------------------------------------
------------------------------------------------------
Slot Type
------------
method: GET
url: https://database-api-latest.onrender.com/myapp/slot_type/?slot_id=[number]

Successful output:
{
  "slot type is ": "inner"
}

Bad output: (Status: 403 Forbidden)
slot does not exist



------------------------------------------------------
------------------------------------------------------
Authenticate User
------------
method: GET  
url: https://database-api-latest.onrender.com/myapp/authenticate_user/?username=[username]&password=[password]

Successful output:
{
  "success": true,
  "user": {
    "id": 1,
    "username": "One",
    "password": "test1"
  }
}

Bad output: (Status 403 Forbidden)
Invalid Credentials


------------------------------------------------------
------------------------------------------------------
Add User
------------
method: POST 
url: https://database-api-latest.onrender.com/myapp/add_user/
body: {
  "username": "two",
  "password": "test2"
}

Successful output:
{
  "message": "User added successfully"
}

Bad output: (Status 403 Forbidden)
User already Exists


------------------------------------------------------
------------------------------------------------------
Remove Reservation
------------
method: DELETE
url: https://database-api-latest.onrender.com/myapp/remove_reservation/
body: {
	"slot_id": [number]
}

Successful output:
{
  "message": "Reservation removed successfully"
}

Bad output: (Status 403 Forbidden)
No such Reservation


------------------------------------------------------
------------------------------------------------------
Get Your Reservations
------------
method: GET 
url: https://database-api-latest.onrender.com/myapp/get_your_reservations/?username=[username]

Successful output (example):
{
  "reservations": [
    {
      "id": 2,
      "price": 0.43200000000000005,
      "expiry": "2024-04-02T23:19:27.055Z",
      "Slot_ID_id": 23,
      "userID_id": 1
    }
  ]
}

Bad output:
{
  "reservations": []
}

------------------------------------------------------
------------------------------------------------------
Add Reservation
------------
method: POST
url: https://database-api-latest.onrender.com/myapp/add_reservation/
body: {
	"username": [user's username],
	"slot_id": [number],
	"expiry_hours": [number of hours]
}

Successful output:
{
  "message": "Reservation added successfully"
}

Bad output:
{
  "error": "Slot is already booked"
}
or
{
  "error": "Slot not found"
}

