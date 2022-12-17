from flask import Flask

app = Flask(__name__)


@app.route("/ping")
def ping():
    return "Hello There!!"


@app.route("/testing")
def testing():
    return {"data1":"data1","data2":"data2","data3":"data3","data4":"data4","data5":"data5","data6":"data6","data7":"data7 "}

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=3000)
