from flask import Flask

app= Flask(__name__)

@app.route('/users', methods =['POST'])
def create_user():
    return "x"




if __name__ == '__main__':
    app.run(port=80, debug=True)