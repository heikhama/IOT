import bcrypt

password = "admin123"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('admin', hashed_password))