from flask import Flask, request
import execution_engine

app = Flask(__name__)

@app.route('/gorilla_interpreter', methods=['GET'])
def gorilla_interepreter():
    try:
        request_content = request.get_json()
        code = request_content['code']
        result = execution_engine.python_containerize_and_execute(code)
        return result, 200
    except Exception as e:
        return "unable to execute with error message {e}".format(e=e), 500
    

@app.route('/gorilla_sql_interpreter', methods=['GET'])
def gorilla_sql_interpreter():
    try:
        request_content = request.get_json()
        code = request_content['code']
        client_config = request_content['client_config']
        result =  execution_engine.sql_execute(code, client_config=client_config)
        return result, 200
    except Exception as e:
        return "unable to execute with error message {e}".format(e=e), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=433)
    #app.run(host="0.0.0.0", port=443, debug=True)
