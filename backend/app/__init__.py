from flask import Flask

app = Flask(__name__)

@app.route('/')
def default():
	return 'Welcome to the blockchain'

# by default on port 5000
# app.run()
app.run(port=5001)