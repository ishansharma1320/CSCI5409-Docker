from flask import Flask
from modules.summationAPI import summation_api_bp
def create_app():
    app = Flask(__name__)
    app.debug=True

    app.register_blueprint(summation_api_bp,url_prefix='/summation')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0',port=7000)


    # JSON Validation (keys present)
    # File Exists or not
    # Format of File whether in csv or not
        # check if product and amount are in columns
        # check if all rows in df have values and are not NaN or empty

