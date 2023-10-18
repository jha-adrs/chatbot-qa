import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
file_format='txt'
def establish_db_connection():
    try:
        conn = pymysql.connect(user=os.getenv('DATABASE_USER'),
                               password=os.getenv('DATABASE_PASSWORD'),
                               database=os.getenv('DATABASE'),
                               host=os.getenv('DATABASE_HOST'))
        return conn
    except pymysql.Error as e:
        print("Error: Unable to connect to the database.", e)
        return None

def fetch_data_from_database(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT q.questiontext, a.answertext FROM questions q LEFT JOIN answers a ON a.questionid = q.questionid WHERE a.answertext IS NOT NULL "
            cursor.execute(query)
            data = cursor.fetchall()
            print(f"Successfully fetched rows " , data)
            return data
    except pymysql.Error as e:
        print(f"Error: Unable to fetch data  .", e)
        return []

def save_to_csv(data):
    print(f"Saving data  to CSV...")
    if not os.path.exists('processed'):
        os.makedirs('processed')
    file_path = os.path.join('text', f'data.{file_format}')
    df = pd.DataFrame(data, columns=['question', 'answer'])
    df.to_csv(file_path, index=False)
    print(f"Data saved to '{file_path}'")
    print("--------------------------------------------------")
    return

def create_scrape():
    print("Starting scrape...")
    os.system('python3 scrape.py')
    print("Scrape complete.")
    print("--------------------------------------------------")
    return

def main():
    print("Starting context extractor...")
    
    conn = establish_db_connection()
    if conn:
        data = fetch_data_from_database( conn)
        if data:
            save_to_csv(data, )
        else:
            print(f"No data found  ")
               
        conn.close()
        # Created scraped data file in csv
        print("--------------------------------------------------")
        create_scrape()

    else:
        print("Exiting due to database connection error.")

if __name__ == "__main__":
    main()
