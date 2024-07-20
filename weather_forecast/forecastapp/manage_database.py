import psycopg2


def get_db_connection():
    """Устанавливает соединение с базой данных PostgreSQL."""
    return psycopg2.connect(
        dbname='weather_db',
        user='user',
        password='password',
        host='db',  # Имя сервиса из docker-compose
        port='5432'
    )


def add_city(name, latitude, longitude):
    """Добавляет город в базу данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cities (name, latitude, longitude)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) 
        DO UPDATE SET latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude;
    ''', (name, latitude, longitude))
    conn.commit()
    cursor.close()
    conn.close()


def get_city_coordinates(name):
    """Получает координаты города из базы данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT latitude, longitude FROM cities WHERE name = %s', (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def get_all_cities():
    """Получает все уникальные названия городов из базы данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM cities')
    cities = cursor.fetchall()
    cursor.close()
    conn.close()
    return [city[0] for city in cities]  # Возвращаем список названий городов


def get_search_history(user_ip):
    """Получает историю поисков для указанного IP-адреса."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city_name, search_count 
        FROM city_searches
        WHERE user_ip = %s
    ''', (user_ip,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'city_name': row[0], 'search_count': row[1]} for row in history]


def update_search_count(city_name, user_ip):
    """Обновляет счетчик поисков для указанного города и IP-адреса."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO city_searches (city_name, user_ip, search_count)
        VALUES (%s, %s, 1)
        ON CONFLICT (city_name, user_ip)
        DO UPDATE SET search_count = city_searches.search_count + 1;
    ''', (city_name, user_ip))
    conn.commit()
    cursor.close()
    conn.close()
