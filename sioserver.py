import redis

from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

REDIS_URI = 'redis://redis/1'

client = redis.from_url(REDIS_URI)


async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
async def user_online(sid, message):
    client.set(sid, message['data'])
    print('online status saved to redis: ' + sid)
    await sio.emit('my_response', {'data': 'user saved into redis'}, room=sid)


@sio.event
async def connect(sid, environ):
    print('user connected: ' + sid)
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
async def my_event(sid, message):
    print('client sent message: ' + message['data'])
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    client.delete(sid, 'username')


app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
