# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:37:45 2019

@author: Abner
"""

from flask import Flas
import connexion

app = connexion.App(__name__, specification_dir='./')
#read the swagger.yml file to configure the endpoints
app.add_api('swagger3.yml',base_path='/api')


if __name__ == "__main__": 
	app.run(debug=True)