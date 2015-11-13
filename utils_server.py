#!/bin/python
# Services exposed by the VM Manager
# The REST url :
# http://host-name/api/1.0/disk-usage
# http://host-name/api/1.0/running-time
# http://host-name/api/1.0/mem-usage
# http://host-name/api/1.0/running-processes
# http://host-name/api/1.0/cpu-load
# http://host-name/api/1.0/execute/<command>
import urlparse
import os
import os.path
import json
# bunch of tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import Get_issues
import logging
define("port", default=8000, help="run on the given port", type=int)
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
class Org_based_search(tornado.web.RequestHandler):
    def get(self):
		self.render('org.html')
    def post(self):
        post_data = dict(urlparse.parse_qsl(self.request.body))
        c = Get_issues.Get_issues()
        c.get_all_issues('org',str(post_data['organization']),None)
        c.write_all_issues_to_a_file_after_applying_filter(post_data['labels'])
        self.render('result.html')
#	    self.write(c.create_instances(post_data['number_of_vm']))
#
#        c.filter_issues_with_lables(post_data['labels'])
#		if(result == True):
#		print "Got request for "+post_data['number_of_vm']+"VMs"

class Institiue_based_search(tornado.web.RequestHandler):
    def get(self):
		self.render('institute.html')


class Lab_based_search(tornado.web.RequestHandler):
    def get(self):
		self.render('labs.html')

#class VMDetails(tornado.web.RequestHandler):
#    def get(self, command):
#    	result = c.get_instances_on_vpc('vpc-9aa038ff')
#	if(result == True):
#	    self.render('result.html')


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[
			(r"/", MainHandler),
            (r"/Org_based_search", Org_based_search),
            (r"/Institiue_based_search", Institiue_based_search),
            (r"/Lab_based_search", Lab_based_search)
#			(r"/VMDetails", VMDetails)
		],
		template_path=os.path.join(os.path.dirname(__file__), "templates"),debug = True)
	http_server = tornado.httpserver.HTTPServer(app)
	current_file_path = os.path.dirname(os.path.abspath(__file__))
	options.port = 8080
	logging.info("utils_server: It will run on port : "+str(options.port))
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
