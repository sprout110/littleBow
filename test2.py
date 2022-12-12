from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from user import *
from home import *

Brain = user.UserSay("test", "k2412")
returnMessages = Brain.process()