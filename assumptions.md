# Project Assumptions
This file contains a list of every assumption made to cover all possible cases presented to the functions in the project. These assumptions have been placed under the heading corresponding to the section of the software they influence. These assumptions also only hold true for the current spec and may change if the spec changes in the future

## Common Assumptions
- There is only 1 slack owner which is the first user created and this cannot be changed afterwards
- The slack owner will have the a user id value of 0
- If an AccessError and InputError occur at the same time, an AccessError will be returned first

## Authorisation Assumptions
- u_id is unique to each user and persistent between sessions
- token from each auth function is unique to every user and persistent between sessions
- auth_logout() currently returning false when given invalid token rather than raising AccessError

## Message Functions Assumptions
- When sending an empty message, an input error is raised. This is because it can lead to accidental message spam.
- Editing a message can raise an InputError if the message is greater then 1000 characters or the message id doesnt exist
- For react functions, if the user reacts to a function they are not a member of it raises an AccessError
- When pinning a message, only a slack owner can use this and not a channel owner (owner is not differentiated well in spec)

## User Functions Assumptions
- u_id is an integer between 0 and 65535
- Falsy values (Empty/None) are not permitted to be used as first/last names, emails, handles
- Whitespace characters are not permitted to be used as first/last names, emails, handles
- If a user attempts to reuses their email when changing their email it will fail (conservation of resources)
- If a user attempts to reuse their handle when changing their handle it will fail
- In upload photo, the value of x_start and y_start must be less then x_end and y_end respectively

## Channel Functions Assumptions
- channel_id is an integer between 0 and 65535
- When a user creates a channel, they are automatically added to it as an owner
- channel_id is the only field that must be unique for a channel
- if an AccessError and InputError occur at the same time, an AccessError will be returned first
- When an owner of a channel tries to remove the slack owner as an owner from a channel, a AccessError is returned
- Slack owner will be classified as a owner of every channel they are in rather than just having admin permissions without owner role
- A user can call removeowner on themselves to take away their owner privildges but the slack owner will be given an AccessError, since this will break the assumption above
- The functions channel_addowner and channel_removeowner can also raise an InputError if the given u_id is not a valid existing user
- For channel_invite() a valid user is considered to an existing user who is not already in the channel. This also applies to channel_join() since joining is equivalent to inviting self
- Using channel_addowner on a user who is not a member of the channel will automatically add them and make them an owner
- channels_listall() will return all channels including private channels

## Other Functions Assumptions
- When searching for a string, results will only appear as a match if the entire word matches the query exactly. An example of this is the query 'a' will not match 'ab' and the query 'I thin' will not give any match to 'I think'.
