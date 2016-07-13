#!/usr/bin/env python3

import requests
import json
import os
import sys
import frontmatter
import datetime


class Migrate( object ):
	def __init__( self ):
		super( Migrate, self ).__init__()

		self.github_link = 'http://api.github.com/repos/nwjs/website/contents/src/blog'

		posts = self.get_file_list()

		for post in posts:
			download = self.download_post( post['download_url'] )
			content = self.parse_post( download )

			self.create_post( post['name'], content )


	def get_file_list( self ):
		request = requests.get( self.github_link )

		return json.loads( request.text )


	def download_post( self, post_url ):
		return requests.get( post_url ).text


	def parse_post( self, content ):
		post = frontmatter.loads( content )		
		post['layout'] = 'post'
		post.content = post.content.replace('{{{', '{{').replace('}}}', '}}') 

		return frontmatter.dumps( post )

	def create_post( self, name, content ):
		os.chdir( os.path.dirname( sys.path[0] ) )

		try:
			post = frontmatter.loads( content )
			date = datetime.datetime.strptime( post['date'], '%Y/%m/%d' )
			postname = '_posts/{date}-{filename}'.format(date=datetime.date.strftime( date, '%m-%d-%y' ), filename=name)
			content = self.parse_post( content )

			with open( postname, 'a+' ) as file:
				file.write( content )

			print('File created: {filename}'.format(filename=postname))

		except Exception as error:
			raise error

if __name__ == '__main__':
	Migrate()