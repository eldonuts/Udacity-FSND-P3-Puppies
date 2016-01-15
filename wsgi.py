from puppies import app

from puppies.config import configure_app
configure_app(app)

ip = app.config.get('SERVER_IP')
port = app.config.get('SERVER_PORT')

if __name__ == '__main__':
    app.run(host=ip, port=port)
