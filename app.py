import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
from eqdata import show_data, write_data, search
env = Environment(loader=FileSystemLoader('html'))


class EquityTopTEn(object):
    @cherrypy.expose
    def index(self):
        eqdata = show_data()
        heading = write_data()
        tmpl = env.get_template('index.html')
        return tmpl.render(heading=heading, eqdata=eqdata)

    @cherrypy.expose
    def generate(self, q):
        result = search(q)
        heading = write_data()
        tmpl = env.get_template('search.html')
        return tmpl.render(result=result, heading=heading)


if __name__ == '__main__':
    cherrypy.engine.housekeeper = cherrypy.process.plugins.BackgroundTask(21600, write_data())
    cherrypy.engine.housekeeper.start()
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 80)),
        },
        '/assets': {
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'assets',
        }
    }

    cherrypy.quickstart(EquityTopTEn(), '/', config=config)
