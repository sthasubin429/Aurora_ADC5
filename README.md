# Aurora_ADC5
Travelers Journal Project By Aurora From ADC5

Our Group includes:
    Ishan Shrestha (NP03A180083)
    Rajesh Kawan   (NP03A180090)
    Smita Shrestha (NP03A180080)
    Subin Shrestha (NP03A180072)

Login details

for admin
username: root
password: admin


for normal users

username: sthsubin
password: subin

username: ishan
password: ishan

username: rajesh
password: rajesh

username: smita
username: smita

#####################################################
#####################################################
API Documentation

Name: Read All
Request: GET
URL: http://127.0.0.1:8000/api/posts/read/
Function: Returns all the post

Name: Read All
Request: GET
URL: http://127.0.0.1:8000/api/posts/read/33/
Function: Returns specific post on the basis of post id

Name: Read with pagination
Request: GET
URL: http://127.0.0.1:8000/api/posts/read/pagination/5/1/
Function: Returns posts depending upon size and page number

Name: Read with user
Request: GET
URL: http://127.0.0.1:8000/api/posts/read/user/3/
Function: Returns all the post posted by the given user

Name: Read with user
Request: GET
URL: http://127.0.0.1:8000/api/posts/read/user/3/
Function: Returns all the post posted by the given user

Name: Create post
Request: Post
URL: http://127.0.0.1:8000/api/posts/create/
JSON Format:
    {
    "title": "Enter Title Here",
    "content": "Enter Your content Here",
    "username": "Enter username here"
    }
ps: username must be valid,
valid username but not limited to {sthsubin, rajesh, ishan, smita, ram}

Return:
    {
    "message": "Post Sucessfully Created!!!"
    }

Name: Update Post
Request: Post
URL: http://127.0.0.1:8000/api/posts/create/
JSON Format:
    {
  "title": "Enter Updated Title Here",
  "content": "Enter Updated Your content Here"
    }
Return:
    {
    "message": "Successfully updated!!"
    }

Name: Delete Post
Request: Delete
URL: http://127.0.0.1:8000/api/posts/delete/36

Return:
    {
    "message": "Post Deleted"
    }
