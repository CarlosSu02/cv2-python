
# from config import config

from app import init_app
app, socketio = init_app()

if __name__ == '__main__':

    # app.config.from_object(config)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
