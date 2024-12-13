from flask import Flask, render_template, request, jsonify
import pickle 
import numpy as np


app = Flask(__name__)


def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['GET', 'POST'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.get("touchscreen", "off") == "on"
        ips = request.form.get("ips", "off") == "on"

        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(bool(touchscreen))
        feature_list.append(bool(ips))

        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2in1convertible', 'gaming', 'notebook', 'ultrabook', 'netbook', 'workstation']
        opsys_list = ['linux', 'mac', 'windows', 'other']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        # for item in company_list:
        #     if item == company:
        #         feature_list.append(1)
        #     else:
        #         feature_list.append(0)

        # print(feature_list)

        def traverse(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)

        pred = prediction(feature_list) * 304.39
        pred = np.round(pred[0], 2)

    return render_template("index.html", pred = pred)


if __name__ == '__main__':
    app.run(debug=True)
