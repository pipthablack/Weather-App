from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_migrate import Migrate
app = Flask(__name__,template_folder='templates')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.ecom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate=Migrate(db,app)

class City(db.Model):
    __tablename__= 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)


@app.route('/',methods=['GET', 'POST'])
def index():
    new_city = request.form.get('city')

    if request.method == 'POST':
        if new_city is not None:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
        





    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
        
    weather_data =[]
   
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        print(r)
        wj=r['weather'].json
        print(wj)
        
        weather = {
        
        'city': city.name ,
        'temperature' : r['main']['temp'],
        #'temperature' : r['main'],
        #'description' : r['weather'[0]]['description'],
        'icon' : r[0]['icon']
    }
   
        weather_data.append(weather)
    return  render_template('weather.html', weather_data=weather_data)



if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()