from siteCode import db, bcrypt
from siteCode.models import User, Game
import os

keep_files = ["1.exe", "1.png"]

db.drop_all()
db.create_all()

##### defult user

hashed_pw = bcrypt.generate_password_hash("p123456").decode("utf-8")
new_user = User(username="danielY", email="yavn.daniel@gmail.com", password=hashed_pw)
db.session.add(new_user)
#base_game = Game(id=1, name="basic", description="basic", uploader=new_user, cost=0.0,image="games_img/1.png")
#db.session.add(base_game)
#new_user.games_uploaded.append(base_game)

# clean games
os.chdir("siteCode/games/")
for game_path in os.listdir("."):
    if os.path.basename(game_path) not in keep_files:
        os.remove(game_path)
        print game_path

os.chdir("../static/games_img/")
for img_path in os.listdir("."):
    if os.path.basename(img_path) not in keep_files:
        os.remove(img_path)
        print img_path

db.session.commit()
