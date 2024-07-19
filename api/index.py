from flask import Flask, jsonify, json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello world! :D'



if __name__ == '__main__':
    app.run()
