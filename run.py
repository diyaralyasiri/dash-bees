from app.data_analysis.graphing import bokeh_worker, filtered_graphs
from multiprocessing import Process
from app import app
from flask_cors import CORS


if __name__ == "__main__":
    # Process(target=bokeh_worker).start()
    cors = CORS(app, resources={r"/dashboard/": {"origins": "diyartest.herokuapp.com"}})
    app.run(debug=False, port=5000)