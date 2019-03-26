import subprocess, os
from siteCode import crypto, models, db
import commands

decryptor_path = os.path.abspath(r".\siteCode\ready_blockers\decryptor.cs")


def compile_blocker(blocker_path, e_game_path, id_path):
    ces_path = r'"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\Roslyn\csc.exe"'
    new_file = blocker_path
    code_file = e_game_path
    id_file = id_path
    blocker_code_file = decryptor_path

    command = ces_path + \
              " /out:" + new_file + \
              " /res:" + code_file + ",code,private  " + " /res:" + id_file + ",id,private " + \
              "/reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll " + \
              blocker_code_file
    print command

    x = subprocess.call(command, shell=False)
    if x:
        print "there was a compilation error"
        print x



def create_id_file(id):
    id_dir = "./siteCode/egames/"
    id_path = os.path.abspath(id_dir + "id_" + str(id))
    f = file(id_path, "wb")
    f.write(str(id))
    f.close()
    return id_path


def create_new_blocker(user, game_id):
    games_dir = "./siteCode/games/"
    game_path = os.path.abspath(games_dir + str(game_id) + ".exe")
    redy_blocker = os.path.abspath(r".\siteCode\ready_blockers\\" + str(user.id)+str(game_id) + ".exe")
    #G:\cyber\Final_Cyber_Project\MileStones\Site\siteCode\ready_blockers
    print "rblocker ",redy_blocker
    # encrypt file
    e_dict = crypto.encrypt2(game_path)

    # create GameDownloaded
    game = models.GameDownload(Crypto_key=e_dict["key"], Crypto_iv=e_dict["iv"], user_id=user.id)
    user.games_downloaded.append(game)
    db.session.flush()  # needed?

    # create id fie
    id_path = create_id_file(game.id)

    db.session.commit()  # ^

    # compile
    compile_blocker(redy_blocker, e_dict["encrypted_code_path"], id_path)
    return redy_blocker
    # return download_and_remove(e_dict["encrypted_code_path"], filename)
