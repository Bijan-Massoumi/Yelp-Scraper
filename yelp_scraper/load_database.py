import sqlite3
import json

if __name__ == "__main__":
    city = "Davis"
    filename = "crawled_data/" + city + "_items.json"
    database = "databases/" + city + ".db"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try: 
        c.execute('''CREATE TABLE restaurants
                 (cuisine text, name text, neighborhood text, stars real, numberOfReviews integer,url text,id id integer PRIMARY KEY,address text,author text,review_stars float,review_body text,review_date text,price text )''')
    except Exception as e:
        c.execute('''DROP TABLE restaurants''')
        c.execute('''CREATE TABLE restaurants
                 (cuisine text, name text, neighborhood text, stars real, numberOfReviews integer,url text,id INTEGER PRIMARY KEY AUTOINCREMENT,address text,author text,review_stars float,review_body text,review_date text,price text )''')

    with open(filename) as f:
        for line in f:
            item = json.loads(line)
            c.execute("INSERT INTO restaurants(cuisine,name,neighborhood,stars,numberOfReviews,url,address,author,review_stars,review_body,review_date,price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (tuple(item["cuisine"]),item["name"],item["neighborhood"]
                item["stars"].split(' ')[0]), item["numberOfReviews"],item["url"],item["address"],item['author'],item["review_body"],item["review_date"],item["price"])
        conn.commit()

    for row in c.execute('SELECT * FROM restaurants ORDER BY id'):
        print row




