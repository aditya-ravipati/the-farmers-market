from flask import Flask
import logging as logger
from api import *

logger.basicConfig(level="DEBUG")

flaskInstance = Flask(__name__)

if __name__=='__main__':
    logger.debug("Starting the application")
    flaskInstance.run(host='0.0.0.0', port=5000, debug=True)
