#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")

class RezultatHandler(BaseHandler):
    def post(self):
        rezultat = self.request.get("vnos")
        params = {"rezultat": rezultat}
        self.render_template("rezultat.html", params)

class KalkulatorHandler(BaseHandler):
    def post(self):
        calc = self.request.get("vnos1")
        calc2 = self.request.get("vnos2")
        operacija = self.request.get("operacija")
        if operacija == "+":
            rezultat = float(calc) + float(calc2)
        elif operacija == "-":
            rezultat = float(calc) - float(calc2)
        elif operacija == "/":
            rezultat = float(calc) / float(calc2)
        elif operacija == "*":
            rezultat = float(calc) * float(calc2)


        params = {"calc": calc, "calc2": calc2, "operacija": operacija, "rezultat": rezultat}
        self.render_template("kalkulator.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/kalkulator', KalkulatorHandler)
], debug=True)
