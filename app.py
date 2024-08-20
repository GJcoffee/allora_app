import time

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

    try:
        # Check if the host_id already exists
        existing_host = Host.query.filter_by(host_id=data['host_id']).first()

        if existing_host:
            # If the host_id exists but the IP is different, update the host_ip
            if existing_host.host_ip != data['host_ip']:
                existing_host.host_ip = data['host_ip']
                db.session.commit()
                return jsonify({"message": "Host IP updated successfully"}), 200
            else:
                return jsonify({"message": "No changes detected"}), 200
        else:
            # If host_id does not exist, create a new record
            new_host = Host(host_id=data['host_id'], host_ip=data['host_ip'])
            db.session.add(new_host)
            db.session.commit()
            return jsonify({"message": "Host information uploaded successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    while True:
        try:
            time.sleep(10)
            app.run(debug=False, host='0.0.0.0', port=5500)
            break
        except Exception as e:
            print(e)
        finally:
            time.sleep(2)