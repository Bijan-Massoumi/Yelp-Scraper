import sqlite3
import json

if __name__ == "__main__":
    city = "slo"
    filename = "crawled_data/" + city + "_items.json"
    database = "databases/" + city + ".db"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try: 
        c.execute('''CREATE TABLE restaurants
                 (cuisine text, name text, neighborhood text, stars text, numberOfReviews integer,url text,id INTEGER PRIMARY KEY AUTOINCREMENT,address text,author text,review_stars text,review_body text,review_date text,price text,uuid text );''')
    except Exception as e:
        c.execute('''DROP TABLE restaurants;''')
        c.execute('''CREATE TABLE restaurants
                 (cuisine text, name text, neighborhood text, stars text, numberOfReviews integer,url text,id INTEGER PRIMARY KEY AUTOINCREMENT,address text,author text,review_stars text,review_body text,review_date text,price text,uuid text );''')

    with open(filename) as f:
        for line in f:
            item = json.loads(line)
            itemTuple = (" ".join(item["cuisine"]),item["name"],item["neighborhood"],float(item["stars"].split(' ')[0]),
                int(item["numberOfReviews"]),item["url"],item["address"],item['author'],float(item['review_stars']),item["review_body"],
                item["review_date"],item["price"],item["ID"])
            #print itemTuple
            
            c.execute(u"""INSERT INTO restaurants(cuisine,
                name,
                neighborhood,
                stars,
                numberOfReviews,
                url,
                address,
                author,
                review_stars,
                review_body,
                review_date,
                price,
                uuid) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);""",itemTuple)
    conn.commit()

    for row in c.execute('SELECT COUNT(*),numberOfReviews,name, AVG(review_stars), stars FROM restaurants GROUP BY uuid'):
        print row
        print "\n"



