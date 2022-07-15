import socketio
import eventlet

## creates a new Async Socket IO Server
sio = socketio.Server(async_mode='eventlet')
## Creates a new Aiohttp Web Application
app = socketio.WSGIApp(sio, static_files={'/': 'index.html'})
# app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
# sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
#async def index(request):
#    with open('index.html') as f:
#        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, wsgi_environ, auth):
    print(sid)
    # Attach data to SID by
    # https://python-socketio.readthedocs.io/en/latest/server.html#user-sessions
    print(wsgi_environ)
    print(auth)
    sio.emit('back', sid, wsgi_environ, auth)


## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.event
def send_message(sid, *message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: ", sid)
    print(message)
    for i in message:
        print(i, type(i))
    sio.emit('back', message, to=sid)


## We bind our aiohttp endpoint to our app
## router
# app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)