Summary
=======

Redirects standard input/output of a command into a Matrix room.

```
pipe2matrix --homeserver <homeserver url> --auth_token <auth token> --admin_id <userid> [--admin_id <userid>...] ( --room_name <room name> | --room_id <room id> ) [--wait] [--log <log file>] [--] ( - | command args... )
```

`pipe2matrix` is somewhat similar to `netcat`, but for matrix. On the matrix
side, `pipe2matrix` will either join an existing room, or will create a new room
and invite the given ("admin") user(s) to the new room. On the local side,
`pipe2matrix` will either start a given program, or will use its own standard
input/output. After that, `pipe2matrix` will send all output of the child
program as messages into the matrix room, and will feed all messages in the
room as input into the child program. Once the child program completes,
`pipe2matrix` will exit too.


Command-line arguments
----------------------
 
* `--homeserver <homeserver url>` The URL of the Matrix server with the bot's user account.
* `--auth_token <auth token>` The authentication token of the bot's user account.
  See https://t2bot.io/docs/access_tokens/ for the instructions on how to get the auth token.
* `--admin_id <userid>` The id of the user that should be invited by the bot. The `--admin_id` flag
  can be repeated multiple times, and each mentioned user will be invited into the room. This flag
  is ignored if joining an existing room.
* `--room_name <room name>` The name of the room that will be created. This is incompatible with
  the `--room_id` option.
* `--room_id <room id>` The room id of the room to talk in. The bot will try to join the room if it
  is not already in it. This is incompatible with the `--room_name` option.
* `--wait` If this flag is present, the bot will not run the command until
  at least one of the invited users have joined the room, or until all have
  declined the invitation (in which case the bot will quit without ever
  running the command). The flag is ignored if joining an existing room.
* `--log <log file>` The file to send the log to. If not present, log messages are printed to stderr.
  Because this is an early development, there are a lot of log messages...
* `command` The command to run. If `command` is a single dash "-", the bot will pass its own standard
  input/output to/from the matrix room.

Caveats
-------
 
* End-to-end encryption is currently unsupported. I am not sure how much the interface will have
  to change to support it: `pipe2matrix` will probably need a persistent storage for the
  encryption keys; it is possible that authentication will have to be done with username
  and password instead of auth token.
* `pipe2matrix` uses a heuristic to break the continuous output stream
  into messages. Currently:

  - Each line of output is a separate message.
  - If there is no new output for 5 seconds, an unfinished line of output will
    also be sent as a message.

* There is no way to control the bot itself: all input is redirected to the child command.
  For example, there is no way to kill the command via Matrix interface.

  One notable exception: if you log in as bot and leave the room, the bot will send EOF to the
  subprocess or to the bot's stdout.

Contact
-------

If you do use `pipe2matrix`, I'd appreciate if you let me know! You can find me on Matrix:
 - @anton:rendezvous.anton.molyboha.me
 - @anton.molyboha:matrix.org
By e-mail:
 anton.stay.connected@gmail.com
Or [create an issue](https://gitlab.com/anton.molyboha/pipe2matrix/-/issues/new)
