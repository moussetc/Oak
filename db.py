import MySQLdb
from config import host, user, password, database
from names import POKEMON, RAID
import datetime, calendar

database = MySQLdb.connect(host,user,password,database)
cursor = database.cursor()

cursor.execute('select name from forts')
res = cursor.fetchall()

all_gyms = [i[0].strip() for i in res]


def get_end_time(time):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
    return calendar.timegm(future.timetuple())


def get_pokemon_id(pokemon):
    for lang in POKEMON:
        for p in POKEMON[lang]:
            if POKEMON[lang][p] == pokemon:
                return p


def add_raid(boss, gym, end):
    pokemon_id = get_pokemon_id(boss)
    level = RAID[pokemon_id]

    cursor.execute("select id from forts where name like '%" + str(gym) + "%'")
    res = cursor.fetchall()
    gym_id = res[0][0]

    remaining_minute = int(end.split(':')[1])
    time = get_end_time(remaining_minute)

    query = ("insert into raids ("
            "id, external_id, fort_id, level, pokemon_id, "
            "move_1, move_2, time_spawn, time_battle, time_end)"
            "values "
            "(null, null, " + str(gym_id) + ", " + str(level) + ", "
            + str(pokemon_id) + ", null, null, null, null, "
            + str(time) + ");")
    cursor.execute(query)
    database.commit()


