language = 'FR'

##### LOGS #####
log_level = 'DEBUG'

#####DATABASE, limited to MySQL and MariaDB#####
host = 'localhost'  #host
user = 'root'  #database user
password = 'root'  #database password
database = 'monocle'  #database name

##### DISCORD #####
## ROLES ##

# Roles allowed to use bot admin features (eg. cleaning sectors):
roles_admin = [
        'admin', 
        'Modo',
]

# Those are fake, don't use them
roles_sectors = {
    502697614155392689, # Sector 1
    502406049664304610, # Sector 2
}

# Roles that define a sector
raid_ex_channels = {
    'raid-egg',
    'raid-spam',
    'raid-bacon',
}

## CHANNELS ##
# Channel ID for the welcoming channels for newcomers
assignment_channel = 42424242242424242
# Channel ID for the server rules, linked in the welcome message
rules_channel = 434343434343434343
# Channel ID for raids submissions
raid_channel = 504307932324764852
# Channel ID for quests submissions
quest_channel = 445222271314785492 
