import MySQLdb
from config import host, user, password, database
from names import POKEMON, RAID
from entities import Pokestop
from utils import logger
import datetime, calendar

database = MySQLdb.connect(host,user,password,database)
cursor = database.cursor()

cursor.execute('SELECT name FROM forts')
res = cursor.fetchall()
all_gyms = [i[0].strip() for i in res]

cursor.execute('SELECT id, name FROM pokestops')
res = cursor.fetchall()
# Index ID by name (used for text search)
all_pokestops = {i[1].strip():str(i[0]) for i in res}

def get_end_time(time):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
    return calendar.timegm(future.timetuple())


def get_date():
    today = datetime.date.today() + datetime.timedelta(days=1)
    return calendar.timegm(today.timetuple())


def get_pokemon_id(pokemon):
    for lang in POKEMON:
        for p in POKEMON[lang]:
            if POKEMON[lang][p].lower() == pokemon.lower():
                return p


def add_raid(boss, gym, end):
    pokemon_id = get_pokemon_id(boss)
    level = RAID[pokemon_id]
    if level is None:
        logger.error("No raid level found")
        return

    cursor.execute('SELECT id FROM forts WHERE name = %s', (gym,))
    res = cursor.fetchall()
    gym_id = res[0][0]

    remaining_minute = int(end.split(':')[1])
    time = get_end_time(remaining_minute)

    query = 'INSERT INTO raids (fort_id, level, pokemon_id, time_end) VALUES (%s, %s, %s, %s)'
    logger.debug('Executing query in add_raid \n {}'.format(query), gym_id, level, pokemon_id, time)
    cursor.execute(query, (gym_id, level, pokemon_id, time,))
    database.commit()


def add_quest(pokestop: Pokestop, pokemon):
    pokemon_id = get_pokemon_id(pokemon)

    date = get_date()

    query = 'INSERT INTO quests (fort_id, pokemon_id, date) VALUES (%s, %s, %s)'
    logger.debug('Executing query in add_quest \n {}'.format(query), pokestop.db_id+'("'+pokestop.name+'")', pokemon_id, date)
    cursor.execute(query, (pokestop.db_id, pokemon_id, date,))
    database.commit()

def delete_quest(pokestop: Pokestop):
    query = 'DELETE FROM quests WHERE fort_id = %s'
    logger.debug('Executing query {}'.format(query), pokestop.db_id)
    cursor.execute(query, (pokestop.db_id,))
    database.commit()

