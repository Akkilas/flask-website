from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'fisat pro'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'akkilas'
app.config['MYSQL_DB'] = 'user_registration'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password_input):
            session['user'] = user[1]  # username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('users.html', users=users)


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        cur.execute("UPDATE users SET username=%s, email=%s WHERE id=%s", (uname, email, user_id))
        mysql.connection.commit()
        flash("User updated successfully", "success")
        return redirect(url_for('users'))
    else:
        cur.execute("SELECT * FROM users WHERE id = %s", [user_id])
        user = cur.fetchone()
        return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", [user_id])
    mysql.connection.commit()
    flash("User deleted", "info")
    return redirect(url_for('users'))


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)










