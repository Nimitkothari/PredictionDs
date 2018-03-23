from flask import Flask,send_from_directory,request,Response
from flask_cors import CORS
import os
import json
path = os.getcwd()
print(path)
port = int(os.getenv("PORT", 3030))
upload_folder = path
ALLOWED_EXTENSIONS = set(['pkl','txt','csv'])
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = upload_folder

def train_data(json_data):
    try:
        print("Reading data")
        print("data\n",json_data)
        d = json_data
        #base = []
        #diff = 0
        base1 = d["days"]
        base = d["energy"]
        size = len(base)
        print("size:",size)
        data = set()
        for i in range(size):
            data.add((base1[i],base[i]))
        print("after for loop\n",data)
        # variables to store average
        avgx = 0.0
        avgy = 0.0
        # loop to calculate the average
        for i in data:
            avgx += i[0] / len(data)
            avgy += i[1] / len(data)
        print("avgx\n",avgx)
        print("avgy\n", avgy)

        # least mean square logic to calculate the best fit line
        totalxx = 0
        totalxy = 0
        for i in data:
            totalxx += (i[0] - avgx) ** 2
            totalxy += (i[0] - avgx) * (i[1] - avgy)
        m = totalxy / totalxx
        print()
        b = avgy - m * avgx
        y = d["energy_value"]
        final =str("y = " + str(m) + "x + " + str(b))
        days = str((y - b) / m)
        datafinal=({"energy_value":y,"days":days,"line_equation":final})
        print(datafinal)
        return (json.dumps(datafinal))

    except Exception as e:
        print(e)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json(force=True)
        print("json_data\n",json_data)
        json_object = train_data(json_data)
        print(json_object)
        resp = Response(response=json_object,
                        status=200,
                        mimetype="application/json")
        return resp
    except Exception as e:
        print(e)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)