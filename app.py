from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import db_uri

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy
db = SQLAlchemy(app)


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.String(64), unique=True, nullable=False)
    host_ip = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<Host {self.host_id}>'


with app.app_context():
    db.create_all()


@app.route('/upload', methods=['POST'])
def upload_host_info():
    data = request.get_json()

    # Validate request data
    if 'host_id' not in data or 'host_ip' not in data:
        return jsonify({"error": "Missing host_id or host_ip"}), 400

    # Create a new Host object
    new_host = Host(host_id=data['host_id'], host_ip=data['host_ip'])

    try:
        # Add the new host to the database
        db.session.add(new_host)
        db.session.commit()
        return jsonify({"message": "Host information uploaded successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5500)
