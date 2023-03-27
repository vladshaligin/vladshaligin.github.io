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
import datetime


my_credentials = credentials.Certificate("config.json")
firebase_admin.initialize_app(my_credentials)


subscribers = [
    "cF7wsWvz5Ct2iLV2rXakmQ:APA91bF80_ZFZ5avp-Z-V1wXOQYhnrRmpcfYbF-X8Ky4DXwzHrYvK3iJ9PliQkDsK7_N-XRYSmswv3-btUH0BwB8TG2RYk7EqDdZQf1nE4SHkUWZCIVl5IuIBKoa-zNcM81pYs6Yg-0C"
]


response = messaging.subscribe_to_topic(subscribers, "new_delivery")


routes = web.RouteTableDef()

@routes.get('/get_deliveries')
async def get_deliveries(request: web.Request):
    return web.json_response({"result" : []})

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

def generate_deliveries():
    return


t2 = threading.Thread(target=generate_deliveries)
t2.start()

web.run_app(app, port=os.getenv("PORT", default=5000))