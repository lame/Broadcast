Current Master Branch Build:
[![CircleCI](https://circleci.com/gh/rkk09c/Brodcast/tree/master.svg?style=svg&circle-token=4bb4c3cc6b30eb70d709f012585b11964f5b7a86)](https://circleci.com/gh/rkk09c/Brodcast/tree/master)

# Broadcast

Boradcast is the fix to pesky MMS messages. Broadcast enables you to create groups, add and remove users, schedule events, and save conversation history all through simple SMS messages. Have a group message going but a user wants to add a friend? Broadcast will allow any user of a group to add new people to the group thread so getting together is easy. The new user to the group can even get context of the message thread when they join. Advanced features are a simple text away, you can text Broadcast to schedule an event and start a group with those invited, allowing seemless communication between you and the people that matter.

## Technical Description

Broadcast interfaces with the Twilio programmable messaging API to create a simple and seamless experience for the user. Broadcast has the ability for users to create groups, schedule events through keywords, and manage said groups without the need for an account signup, an internet browser, or an app of any kind. Advanced functionality can be had through the forthcoming web client as well, though it will be purely supplimentary.

## Instillation

### Requirements

Python 3

PostgreSQL (to come)

Docker (to come)

Twilio Account Credentials

### Running local flask server

    $ git clone git@github.com:rkk09c/Brodcast.git
    $ cd Broadcast
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ python manage.py runserver
