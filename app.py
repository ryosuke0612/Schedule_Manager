from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, Event, User, Attendance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    events = Event.query.order_by(Event.date).all()
    return render_template('index.html', events=events)

@app.route('/register_event', methods=['GET', 'POST'])
def register_event():
    if request.method == 'POST':
        title = request.form['title']
        date_str = request.form['date']
        hour = request.form['hours']
        minute = request.form['minutes']
        full_datetime = datetime.strptime(f"{date_str} {hour}:{minute}", "%Y-%m-%d %H:%M")
        new_event = Event(title=title, date=full_datetime)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('register_event', message='イベントを登録しました！'))
    return render_template('register_event.html')

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_details_or_attendance(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        user_name = request.form['user_name']
        status = request.form['status']

        user = User.query.filter_by(name=user_name).first()
        if not user:
            user = User(name=user_name)
            db.session.add(user)
            db.session.flush()  # IDが必要なのでフラッシュ

        existing = Attendance.query.filter_by(user_id=user.id, event_id=event.id).first()
        if existing:
            existing.status = status
        else:
            attendance = Attendance(user_id=user.id, event_id=event.id, status=status)
            db.session.add(attendance)

        db.session.commit()
        return redirect(url_for('event_details_or_attendance', event_id=event.id))

    attendances = Attendance.query.filter_by(event_id=event.id).all()
    return render_template('event_details_or_attendance.html', event=event, attendances=attendances)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
