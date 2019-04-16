from siteCode import db, bcrypt
from siteCode.models import User, Game

db.drop_all()
db.create_all()

##### defult user

hashed_pw = bcrypt.generate_password_hash("p123456").decode("utf-8")
new_user = User(username="danielY", email="yavn.daniel@gmail.com", password=hashed_pw)
db.session.add(new_user)
base_game = Game(id=1, name="basic", description="basic", uploader=new_user)
db.session.add(base_game)
new_user.games_uploaded.append(base_game)

# clean games

db.session.commit()
