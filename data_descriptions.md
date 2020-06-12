## Website Data Descriptions
All data structs used within the website will be described here.

All data related to the website will be stored within 1 dictionary called website_data within website_data.py

This website_data variable is a global variable but can only been interacted with by the interfacing functions provided in website_data.py to create encapsulation and avoid issues in the future

Each data structure needed for the server will be stored as a dictionary entry within website_data where the key is the name of the data struct and the value is a list made up of the corresponding data structure.

Every data structure will also be a dictionary and the layout of these data structure will be described below

# user data

```javascript
{
    "id"            : Unique id for user, integer between 0 - 65535
    "email"         : Email of user, type is string
    "first name"    : First name of user, type is string
    "last name"     : Last name of user, type is string
    "disp name"     : Display name of the user, type is string
    "password"      : Hash of the users password
    "permission id" : integer, follows permission id as outlined in specs
    "img name"      : string that is the name of the image file conatining the users profile picture
    
}
```
# special users
```javascript
[
    list of type user from specifications
]
```

# channel data

```javascript
{
    "id"        : Unique id for channel, integer betweeen 0 - 65535
    "name"      : Name of the channel, string and not unique
    "members"   : List of u_id of users in the channel
    "owners"    : List of u_id of users that are owners of the channel
    "messages"  : List of message ids sent to the channel
    "public"    : Boolean value, if channel is public then True, if private then False
    "standup time" : Time the current standup will finsh, None if no current standup active
    "standup creator" : user id of the user who started the standup
    "standup message" : Collection of all standup messages currently, type is string
    "hangman word"    : The word being guessed for the current active hangman game, None if no active game
    "hangman guesses" : List of letters guessed in the current hangman game

}
```

# message data

```javascript
{
    "id"            : Unique id for message, integer between 0 - 65535
    "sender id"     : id of the user who sent the message
    "channel id"    : id of the channel the message is in
    "contents"      : Contents of the message, string up to 1000 characters
    "timestamp"     : Unix timestamp, type is integer
    "pinned"        : Boolean value, if message is pinned then true
    "reacts"        : list of dictionaries of {'react id' : int, 'user id' : int}
}
```

# valid tokens
i
```javascript
{
    "user id"   : id of the user whos token it belongs to
    "token"     : Token value, hash of email + user id
}
```

# send later

```javascript
[
    List of message data of messages to be sent later
]
```
