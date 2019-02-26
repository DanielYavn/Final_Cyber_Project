from siteCode import db,bcrypt
from siteCode.models import User

db.drop_all()
db.create_all()

##### defult user

hashed_pw = bcrypt.generate_password_hash("p123456").decode("utf-8")
new_user = User(username="danielY", email="yavn.daniel@gmail.com", password=hashed_pw)
db.session.add(new_user)
db.session.commit()

