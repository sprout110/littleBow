from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from module import *
from home import *

Bot = UserSay("test", "k2412")
returnMessages = Bot.process()