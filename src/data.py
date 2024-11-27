import pymysql
import config
import logging

db_settings = {
    "host": config.DB_HOST,
    "port": int(config.DB_PORT),
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "db": config.DB_SCHEMA,
    "charset": "utf8"
}

def search_user(member_data):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
             command = "SELECT * FROM "+config.DB_SCHEMA+"."+config.DB_TABLE+" WHERE email = %s"
             cursor.execute(command, (member_data['email'],))
             result = cursor.fetchone()
             return result
    except Exception as e:
        logging.error(e)
        return 'error'

def update_user(member_data):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor()
        update_query = "UPDATE "+config.DB_TABLE+" SET discord_id = %s WHERE email = %s"
        cursor.execute(update_query, (member_data['discord_id'], member_data['email']))
        if cursor.rowcount > 0:
            conn.commit()
            logging.info(f"Successfully updated the discord_id for {member_data['email']} to {member_data['discord_id']}.")
            return True
        else:
            logging.error(f"No records found for email: {member_data['email']}. No update was made.")
            return False
    except Exception as e:
        logging.error(e)
        conn.rollback()
        return 'error'
