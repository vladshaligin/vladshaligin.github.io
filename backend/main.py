import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import random
import time
from aiohttp import web
import aiohttp_cors
import os
import threading
import random


my_credentials = credentials.Certificate("config.json")
firebase_admin.initialize_app(my_credentials)


deliveries = []

subscribers = [
    "cF7wsWvz5Ct2iLV2rXakmQ:APA91bF80_ZFZ5avp-Z-V1wXOQYhnrRmpcfYbF-X8Ky4DXwzHrYvK3iJ9PliQkDsK7_N-XRYSmswv3-btUH0BwB8TG2RYk7EqDdZQf1nE4SHkUWZCIVl5IuIBKoa-zNcM81pYs6Yg-0C"
]


response = messaging.subscribe_to_topic(subscribers, "new_delivery")


routes = web.RouteTableDef()

@routes.get('/get_deliveries')
async def get_deliveries(request: web.Request):
    return web.json_response({"result" : deliveries})

@routes.post('/accept_delivery')
async def accept_delivery(request: web.Request):
    accept_id = request.rel_url.query['id']
    for delivery in deliveries:
        if delivery["id"] == accept_id:
            deliveries.remove(delivery)
            return web.json_response({"result":"ok"})

app = web.Application()
app.add_routes(routes)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})


for route in list(app.router.routes()):
    cors.add(route)




def add_delivery():
    pizzas = ["Пепперони", "Ассорти", "Европа", "Вегетерианская", "Гавайская", "Моцарелла", "Де Люкс", "Морская"]
    streets = ["Правды", "Лжи", "Ленина", "Катукова", "Есенина"]

    delivery_data = {
        "id": random.randint(0,99999999),
        "pizza": random.choice(pizzas),
        "street": "Ул. " + random.choice(streets) + " д." + str(random.randint(1,60)) + " кв. " + str(random.randint(1,60))
    }

    deliveries.append(delivery_data)

    message = messaging.Message(
        topic="new_delivery"
    )
    response = messaging.send(message)

    print("added new pizza", delivery_data)

def generate_deliveries():
    while True:
        if random.random() < 0.1:
            add_delivery()
        time.sleep(60)


t2 = threading.Thread(target=generate_deliveries)
t2.start()

add_delivery()
add_delivery()

web.run_app(app, port=os.getenv("PORT", default=5000))