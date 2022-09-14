from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flaskproject'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vehicles')
    data = cur.fetchall()
    return render_template('home.html', vehicles = data)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle ():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        registration = request.form['registration']
        location = request.form['location']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO vehicles (make, model, registration, location) VALUES (%s, %s, %s, %s)',
        (make, model, registration, location))
        mysql.connection.commit()
        flash('Vehicle Added Successfully')
        return redirect(url_for('home'))

        

@app.route('/edit/<id>')
def get_vehicle (id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vehicles WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit.html', vehicle = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_vehicle(id):
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        registration = request.form['registration']
        location = request.form['location']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE vehicles
        SET make = %s,
            model = %s,
            registration = %s,
            location = %s
        WHERE id = %s    
    """, (make, model, registration, location, id))
    mysql.connection.commit()
    flash('Vehicle Updated Successfully')
    return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete_vehicle (id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM vehicles WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Vehicle Removed Successfully')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  