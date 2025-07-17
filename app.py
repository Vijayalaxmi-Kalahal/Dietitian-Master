from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Dummy user store
users = {
    'user': 'password'  # Replace with a real user store (e.g., database)
}

# Define models
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'video' or 'chat'
    notes = db.Column(db.Text, nullable=True)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def calculate_bmr(weight, height, age, gender, activity_level):
    if gender == 'Male':
        cal = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'Female':
        cal = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        return None, "Please select a gender."

    activity_multiplier = {
        'Sedentary (little or no exercise)': 1.2,
        'Lightly active (1-3 days/week)': 1.375,
        'Moderately active (3-5 days/week)': 1.55,
        'Very active (6-7 days/week)': 1.725,
        'Super active (twice/day)': 1.9
    }

    if activity_level in activity_multiplier:
        cal *= activity_multiplier[activity_level]
    else:
        return None, "Please select an activity level."

    protein = ['Yogurt (1 cup)', 'Cooked meat (3 Oz)', 'Cooked fish (4 Oz)', '1 whole egg + 4 egg whites', 'Tofu (5 Oz)']
    fruit = ['Berries (80g)', 'Apple', 'Orange', 'Banana', 'Dried Fruits (Handful)', 'Fruit Juice (125ml)']
    vegetable = ['Any vegetable (80g)']
    grains = ['Cooked Grain (150g)', 'Whole Grain Bread (1 slice)', 'Half Large Potato (75g)', 'Oats (250g)', '2 corn tortillas']
    ps = ['Soy nuts (1 Oz)', 'Low fat milk (250ml)', 'Hummus (4 Tbsp)', 'Cottage cheese (125g)', 'Flavored yogurt (125g)']
    taste_en = ['2 TSP (10 ml) olive oil', '2 TBSP (30g) reduced-calorie salad dressing', '1/4 medium avocado', 'Small handful of nuts', '1/2 ounce grated Parmesan cheese', '1 TBSP (20g) jam, jelly, honey, syrup, sugar']

    if cal < 1500:
        meal_plan = [
            ("Breakfast", f"{protein[randint(0, 4)]} + {fruit[randint(0, 5)]}"),
            ("Lunch", f"{protein[randint(0, 4)]} + {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]}"),
            ("Snack", f"{ps[randint(0, 4)]} + {vegetable[0]}"),
            ("Dinner", f"{protein[randint(0, 4)]} + 2 {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]}"),
            ("Snack", f"{fruit[randint(0, 5)]}")
        ]
    elif cal < 1800:
        meal_plan = [
            ("Breakfast", f"{protein[randint(0, 4)]} + {fruit[randint(0, 5)]}"),
            ("Lunch", f"{protein[randint(0, 4)]} + {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]} + {fruit[randint(0, 5)]}"),
            ("Snack", f"{ps[randint(0, 4)]} + {vegetable[0]}"),
            ("Dinner", f"2 {protein[randint(0, 4)]} + {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]}"),
            ("Snack", f"{fruit[randint(0, 5)]}")
        ]
    elif cal < 2200:
        meal_plan = [
            ("Breakfast", f"{protein[randint(0, 4)]} + {fruit[randint(0, 5)]}"),
            ("Lunch", f"{protein[randint(0, 4)]} + {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]} + {fruit[randint(0, 5)]}"),
            ("Snack", f"{ps[randint(0, 4)]} + {vegetable[0]}"),
            ("Dinner", f"2 {protein[randint(0, 4)]} + 2 {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]}"),
            ("Snack", f"{fruit[randint(0, 5)]}")
        ]
    else:
        meal_plan = [
            ("Breakfast", f"2 {protein[randint(0, 4)]} + {fruit[randint(0, 5)]} + {grains[randint(0, 4)]}"),
            ("Lunch", f"{protein[randint(0, 4)]} + {vegetable[0]} + Leafy Greens + {grains[randint(0, 4)]} + {taste_en[randint(0, 5)]} + {fruit[randint(0, 5)]}"),
            ("Snack", f"{ps[randint(0, 4)]} + {vegetable[0]}"),
            ("Dinner", f"2 {protein[randint(0, 4)]} + 2 {vegetable[0]} + Leafy Greens + 2 {grains[randint(0, 4)]} + 2 {taste_en[randint(0, 5)]}"),
            ("Snack", f"{fruit[randint(0, 5)]}")
        ]

    meal_plan_str = '\n'.join([f"{meal}: {items}" for meal, items in meal_plan])
    return cal, meal_plan_str

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'username' not in session:
        return redirect(url_for('login'))

    weight = float(request.form['weight'])
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity_level = request.form['activity_level']

    cal, meal_plan = calculate_bmr(weight, height, age, gender, activity_level)
    if cal is None:
        return redirect(url_for('result', error=meal_plan))

    return redirect(url_for('result', calories=cal, meal_plan=meal_plan))

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = request.args.get('error')
    if error:
        return render_template('result.html', error=error)
    
    calories = request.args.get('calories')
    meal_plan = request.args.get('meal_plan').replace('\\n', '\n')
    return render_template('result.html', calories=calories, meal_plan=meal_plan)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        date_time_str = request.form['date_time']
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        appointment_type = request.form['type']
        notes = request.form.get('notes', '')
        
        appointment = Appointment(username=session['username'], date_time=date_time, type=appointment_type, notes=notes)
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('view_appointments'))
    
    return render_template('schedule.html')

@app.route('/view_appointments')
def view_appointments():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    appointments = Appointment.query.filter_by(username=session['username']).all()
    return render_template('view_appointments.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
