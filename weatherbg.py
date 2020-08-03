import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from sense_hat import SenseHat

import time

# Use the application default credentials
cred = credentials.Certificate("./raspyweather-af308-firebase-adminsdk-shirs-9dc5771da5.json")
firebase_admin.initialize_app(cred)

sense = SenseHat()


db = firestore.client()
doc_ref = db.collection(u'weather log').document(u'2')
doc_time = db.collection(u'weather log').document(u'time')
while True:
    pressure = sense.pressure
    humidity = sense.humidity
    temp = sense.temp

    doc_ref.update({
        u'humidity': int(humidity),
        u'pressure': int(pressure),
        u'temperature': int(temp)})

    doc_time.update({
        u'timestamp': firestore.SERVER_TIMESTAMP
    })

    time.sleep(5)