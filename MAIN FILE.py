import mysql.connector as ms

conn = ms.connect(
    host="localhost",
    user="root", 
    password="utkarsh123#", 
    database="concert")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS staff(
        staff_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        phone_num VARCHAR(15) NOT NULL,
        room VARCHAR(10),
        staff_role VARCHAR(20))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS singers(
        singer_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        singer_name VARCHAR(50) NOT NULL,
        genre VARCHAR(20))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bookings(
    booking_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    concert_date DATE,
    singer_id INT NOT NULL,
    staff_id INT NOT NULL,
    venue VARCHAR(50),
    FOREIGN KEY (singer_id) REFERENCES singers(singer_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id))''')
    
cursor.execute('''INSERT INTO staff (phone_num, room, staff_role)
    VALUES ('+1234567890', 'Room 101', 'Manager')''')

cursor.execute('''INSERT INTO singers (singer_name, genre)
    VALUES ('Harry Styles', 'Pop')''')

cursor.execute('''INSERT INTO bookings (concert_date, singer_id, staff_id, venue)
    VALUES ('2024-11-01', 1, 1, 'The Greens Yard')''')
conn.commit()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if username == "admin" and password == "ilovecs":#username is admin and password is ilovecs
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False

def view():
    cursor.execute("SELECT bookings.booking_id, bookings.concert_date, singers.singer_name, singers.genre, bookings.venue FROM bookings JOIN singers ON bookings.singer_id = singers.singer_id;")
    rows = cursor.fetchall()
    print("-----------------------------------------------------")
    for row in rows:
        print("Booking ID:", row[0])
        print("Date:", row[1])
        print("Singer:", row[2])
        print("Genre:", row[3])
        print("Venue:", row[4])
    print("-----------------------------------------------------")
    
def artist_registration():
    artist_name = input("Enter artist name: ")
    genre = input("Enter genre: ")
    booking_date = input("Enter concert date (YYYY-MM-DD): ")
    venue = input("Enter venue: ")

    cursor.execute("SELECT staff_id FROM staff WHERE staff_id = 1")
    staff_record = cursor.fetchone()
    if not staff_record:
        cursor.execute("INSERT INTO staff (phone_num, room, staff_role) VALUES ('+1234567890', 'Room 101', 'Manager')")
        conn.commit()
        print("backup staff record created.")

    cursor.execute(f"INSERT INTO singers (singer_name, genre) VALUES ('{artist_name}', '{genre}')")
    conn.commit()
    print("Artist registered successfully.")

    cursor.execute(f"SELECT singer_id FROM singers WHERE singer_name = '{artist_name}' AND genre = '{genre}'")
    singer_id = cursor.fetchone()[0]

    cursor.execute(f"INSERT INTO bookings (concert_date, singer_id, staff_id, venue) VALUES ('{booking_date}', {singer_id}, 1, '{venue}')")
    conn.commit()
    print("Booking details added successfully.")

def update():
    print("-----------------------------------------------------")
    singer_id = int(input("Enter artist ID to update: "))
    
    cursor.execute(f"SELECT * FROM singers WHERE singer_id = {singer_id}")
    singer_record = cursor.fetchone()
    
    if singer_record:
        new_name = input("Enter new artist name: ")
        new_genre = input("Enter new genre: ")
        
        query = f"UPDATE singers SET singer_name = '{new_name}', genre = '{new_genre}' WHERE singer_id = {singer_id}"
        cursor.execute(query)
        conn.commit()
        print("Artist details updated successfully!")
    else:
        print("Error Artist with the given ID not found.")
    print("-----------------------------------------------------")
    

def delete():
    print("-----------------------------------------------------")
    singer_id = int(input("Enter artist ID to delete: "))
    
    cursor.execute(f"SELECT * FROM singers WHERE singer_id = {singer_id}")
    singer_record = cursor.fetchone()
    
    if singer_record:
        cursor.execute(f"DELETE FROM bookings WHERE singer_id = {singer_id}")
        conn.commit()
        
        cursor.execute(f"DELETE FROM singers WHERE singer_id = {singer_id}")
        conn.commit()
        
        print("Artist deleted successfully!")
    else:
        print("Error: Artist with the given ID not found.")
    print("-----------------------------------------------------")


def allocate():
    booking_id = input("Enter booking ID: ")
    venue_name = input("Enter venue name: ")

    cursor.execute("SELECT staff_id FROM staff WHERE staff_id = 1")
    staff_record = cursor.fetchone()
    if not staff_record:
        cursor.execute("INSERT INTO staff (staff_id, phone_num, room, staff_role) VALUES (1, '+1234567890', 'Room 101', 'Manager')")
        conn.commit()
        print("backup staff record created.")

    cursor.execute(f"SELECT * FROM bookings WHERE booking_id = {booking_id}")
    booking_record = cursor.fetchone()
    if not booking_record:
        print("Booking ID does not exist.")
        return

    cursor.execute(f"UPDATE bookings SET venue = '{venue_name}' WHERE booking_id = {booking_id}")
    conn.commit()
    print("Venue updated successfully")


def ticket():
    print("-----------------------------------------------------")
    booking_id = int(input("Enter booking ID to calculate bill: "))
    cursor.execute(f"SELECT * FROM bookings WHERE booking_id = {booking_id}")
    booking_record = cursor.fetchone()
    if not booking_record:
        print(f"Error: Booking ID {booking_id} does not exist!")
        return
    ticket_price = float(input("Enter ticket price: "))
    tickets_sold = int(input("Enter number of tickets sold: "))
    total_amount = ticket_price * tickets_sold
    
    print(f"Total bill: ${total_amount}")
    print("-----------------------------------------------------")


def exit_program():
    print("-----------------------------------------------------")
    print("Exiting the program...")
    print("-----------------------------------------------------")
    
def reset():
    cursor.execute("USE concert;")
    cursor.execute("DROP TABLE IF EXISTS bookings;")
    cursor.execute("DROP TABLE IF EXISTS staff;")
    cursor.execute("DROP TABLE IF EXISTS singers;")
    conn.commit()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff(
        staff_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        phone_num VARCHAR(15) NOT NULL,
        room VARCHAR(10),
        staff_role VARCHAR(20))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS singers(
        singer_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        singer_name VARCHAR(50) NOT NULL,
        genre VARCHAR(20))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings(
        booking_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        concert_date DATE,
        singer_id INT NOT NULL,
        staff_id INT NOT NULL,
        venue VARCHAR(50),
        FOREIGN KEY (singer_id) REFERENCES singers(singer_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id))''')

    conn.commit()
    print("Tables have been dropped and recreated successfully. Database reset.")
    print("-----------------------------------------------------")

if not login():
    exit()
while True:
    print("-----------------------------------------------------")
    print("1. VIEW CONCERTS")
    print("2. NEW ARTIST REGISTRATION")
    print("3. UPDATE ARTIST DETAILS")
    print("4. DELETE ARTIST")
    print("5. ALLOCATE VENUE")
    print("6. TICKET SALES AND BILLING")
    print("7. RESET DATABASE")
    print("8. EXIT")
    
    choice = int(input("Enter your choice: "))
        
    if choice == 1:
        view()
    elif choice == 2:
        artist_registration()
    elif choice == 3:
        update()
    elif choice == 4:
        delete()
    elif choice == 5:
        allocate()
    elif choice == 6:
        ticket()
    elif choice == 7:
        reset()
    elif choice == 8:
        print("Exited successfully")
        break
    else:
        print("Invalid choice, please try again.")
    print("-----------------------------------------------------")
