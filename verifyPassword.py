cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
result = cursor.fetchone()
if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
    session['user'] = username
    return redirect('/dashboard')
else:
    return "Invalid credentials"