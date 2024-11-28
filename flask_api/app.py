from flask import Flask
from flask_api.blueprint.bp import app_bp
from init_db import init_neo4j

app = Flask(__name__)
app.register_blueprint(app_bp)

with app.app_context():
    app.neo4j_driver = init_neo4j()

if __name__ == '__main__':
    init_neo4j()
    app.run(host='0.0.0.0', port=5000, debug=True)
