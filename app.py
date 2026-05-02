from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from models import db, Drop
from datetime import datetime, timedelta
import qrcode
import io

app = Flask(__name__)
import os

# Use an environment variable for the database URL if Railway provides one, 
# otherwise default to your local sqlite file.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'instance', 'vraxis.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/drop', methods=['POST'])
def drop_matter():
    content = request.form.get('content')
    expiry_choice = request.form.get('expiry', '24h') 
    
    expiry_map = {'1h': 1, '24h': 24, '7d': 168}
    hours = expiry_map.get(expiry_choice, 24)
    
    new_code = Drop.generate_code()
    expiration = datetime.utcnow() + timedelta(hours=hours)
    
    new_drop = Drop(content=content, code=new_code, expires_at=expiration)
    db.session.add(new_drop)
    db.session.commit()
    
    return redirect(url_for('success', code=new_code))

@app.route('/success/<code>')
def success(code):
    return render_template('success.html', code=code)

@app.route('/qr/<code>')
def generate_qr(code):
    target_url = f"{request.host_url}retrieve?c={code}"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(target_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#d32f2f", back_color="white") 
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/retrieve')
def retrieve_page():
    return render_template('retrieve.html')

@app.route('/api/pickup/<code>')
def pickup_matter(code):
    # EPHEMERAL PROTOCOL: Search and Delete immediately on access
    drop = Drop.query.filter_by(code=code).first()
    
    if drop and datetime.utcnow() < drop.expires_at:
        content = drop.content
        db.session.delete(drop) 
        db.session.commit()
        return jsonify({"content": content})
    
    return jsonify({"error": "Expired or invalid"}), 404

# AdSense required pages
@app.route('/activity')
def activity():
    # Count total drops currently in the system
    drop_count = Drop.query.count()
    # You can also randomize latency slightly to make it feel 'live'
    import random
    latency = f"{random.randint(30, 45)} ms"
    
    return render_template('activity.html', count=drop_count, latency=latency)
@app.route('/journal')
def journal(): return render_template('journal.html')
@app.route('/about')
def about(): return render_template('about.html')
@app.route('/privacy')
def privacy(): return render_template('privacy.html')
@app.route('/terms')
def terms(): return render_template('terms.html')

# The Accountless Essay (Already Done)
@app.route('/journal/the-case-for-the-accountless-web')
def journal_01():
    return render_template('journal_01.html')

# NEW: Infrastructure Essay
@app.route('/journal/za-01-potchefstroom-node')
def journal_02():
    return render_template('journal_02.html')

# NEW: Engineering Essay
@app.route('/journal/the-ember-protocol')
def journal_03():
    return render_template('journal_03.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

