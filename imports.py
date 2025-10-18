from flask import Flask , render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from random import uniform
from datetime import datetime
from threading import Lock
import time