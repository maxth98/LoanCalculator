import warnings
import threading
import queue
import json
import os

from waitress import serve
from multiprocess import cpu_count
from flask import Flask, request, make_response, send_file
from flask_caching import Cache

from annuity import calc_repayment_plan

warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

try:
    with open("configuration.json", "r") as f:
        configuration = json.load(f)
except:
    raise ValueError("Please provide a configuraion.json file!")

app = Flask(__name__)
config = {
    "DEBUG": False,
    "CACHE_TYPE": "SimpleCache",
}
cache = Cache(config=config)
cache.init_app(app)

model_update_queue = queue.Queue()
model_update_event = threading.Event()


@app.route("/calc", methods=["GET"])
def predict_user_questions():
    global configuration
    try:
        params = request.args
        principal = params.get("principal", type=float)
        duration = params.get("duration", type=int)
        nom_intr = params.get("nom_intr", type=float)
        repay_amt = params.get("repay_amt", default=0, type=float)
        period = params.get("period", default="Monatlich", type=str)
        filename = params.get("filename", default="tilgungsplan.xlsx")

        repayment_plan = calc_repayment_plan(principal, nom_intr, duration, repay_amt, period)
        repayment_plan.to_excel(filename)

        filename = os.path.join(os.getcwd(), filename)
        if os.path.isfile(filename):
            return send_file(filename, as_attachment=True)
        else:
            return make_response(f"File '{filename}' not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


if __name__ == '__main__':
    num_workers = cpu_count()
    print("Starting server..")
    serve(app, host='0.0.0.0', port=configuration["port"], threads=num_workers, connection_limit=1000000)
