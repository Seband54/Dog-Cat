from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"  # Replace with a secure, random key in production

# Hardcoded credentials for demonstration purposes
USER_CREDENTIALS = {
    "username": "admin@gmail.com",
    "password": "password123"
}

@app.route('/')
def home():
    # Check if user is logged in
    if session.get("logged_in"):
        return f"Hello, {session.get('username')}! <br><a href='/logout'>Logout</a>"
    # Redirect to login if not authenticated
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        print("Usuario:", username, "Contraseña:", password)  # Depuración
        # Check credentials (for demo purposes)
        if (username == USER_CREDENTIALS['username'] and 
            password == USER_CREDENTIALS['password']):
            # Set session variables
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for('home'))
        else:
            # En lugar de devolver texto plano, rendereamos la misma plantilla con un mensaje de error
            error_message = "Credenciales inválidas"
            return render_template('login.html', error=error_message)
    
    # Render the login form on GET request
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    return "You have been logged out. <a href='/login'>Login again</a>"

if __name__ == '__main__':
    app.run(debug=True)
