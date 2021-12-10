### Command-Line Arguments
python3 backcord.py [color option] [bot status]

`color option` -> NO-COLOR or COLOR. Default COLOR.

bot status -> ONLINE, INVISIBLE, IDLE, DND (Do not disturb). Default ONLINE

### Main Commands
exit -> Exit (lol).

cls -> Clears terminal.

clear -> Clears terminal.

version -> Prints version.

banner -> Prints banner.

stopListen -> Stops listining any channel/dm.


### Server Commands
setServer [server ID] -> Sets the SERVER variable.

listServers -> Lists servers that bot is in.

serverInfo [server ID] -> Gives information about a server.

renameServer [new name] -> Renames the SERVER

leaveServer [server ID] -> Leave the server.

inviteServer [server ID] -> Creates a invite link.

getAuditLogs [max limit] -> Get audit logs of SERVER.


### User Commands
userInfo [user id] -> Gives information about user.

listUsers -> Lists users in SERVER.

changeNick [user id] [new nick] -> Changes in-server nick name of user.

catDm [user id] [message limit] -> Lists messages in user DM. Limit is the max count of messages that will be listed.

dmUser [user id] [message ] ->  Sends a DM message to user.

kickUser [user id] -> Kicks user from SERVER.

banUser [user id] -> Bans user from SERVER.

unbanUser [user id] -> Unbans user from SERVER.

listBanned -> List banned users from SERVER.


### Channel Commands
listChannels -> Lists channels in the SERVER.

deleteChannel [channel ID] -> Deletes channel.

renameChannel [channel ID] -> Renames channel.

catChannel [channel id] [message limit] -> Lists messages in channel. Limit is the max count of messages that will be listed.

sendMessage [channel id] [message ] -> Sends message to channel.


### Role Commands
listRoles -> Lists roles in the SERVER.

renameRole [role ID] -> Renames role.

addRole [role ID] [user ID] -> Adds role to user.

removeRole [role ID] [user ID] -> Removes role from user.

deleteRole [role ID] -> Deletes role.

appendAdmin [role name] [user ID] -> Creates a role with "name", gives it OP privs. and appends it to user. 

createRole [role name] [role color] -> Creates a role.


### Bomb Commands
dmAll [spam message] -> Send DM message to all users in SERVER.

dmSpam [user ID] [spam message] -> Spam DM message to user.

bombRoles -> Deletes all the roles in SERVER.

spamRole [role name] -> Spams role.

bombServer -> Bans all the users.

disableRoles -> Disables nearly all permissions of the role.


### Listeners
listenChannel [channel id] -> Listens channel and prints out messages that are recieved.

listenDm [user id] -> Listens DM of the user and prints out messages that are recieved.

listenJoin -> Listens member join/remove events in SERVER.

