import subprocess, os
from siteCode import crypto, models, db
from datetime import datetime

decryptor_path = os.path.abspath(r".\siteCode\ready_blockers\decryptor.cs")
decryptor_no_enc_path = os.path.abspath(r"./siteCode/ready_blockers/decryptor_noenc.cs")


def compile_blocker(blocker_path, e_game_path, id_path):
    """
    compiles new blocker
    :param blocker_path: path fore new blocker
    :param e_game_path: encrypted game file path
    :param id_path: id file path
    :return:
    """
    if os.environ['COMPUTERNAME'] == 'DESKTOP-NDHRRRG':
        ces_path = r'"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\Roslyn\csc.exe"'  # home
    else:
        ces_path = r'"C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn\csc.exe"'  # cyber
    new_file = blocker_path
    code_file = e_game_path
    id_file = id_path
    blocker_code_file = decryptor_path
    rec_pat = "C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\Common7\IDE\Extensions\Xamarin.VisualStudio\Xamarin.Inspector.Windows\Client"
    command = ces_path + \
              " /out:" + new_file + \
              " /res:" + code_file + ",code,private  " + " /res:" + id_file + ",data,private " + "/target:winexe " + \
              "/reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll /reference:System.Windows.Forms.dll " + \
              blocker_code_file
    print command
    try:
        x = subprocess.call(command, shell=False)
    except Exception as e:
        print "there was a compilation error"
        print "massage: ", e.message
        print "comand: ", command
    print "stop"


def create_data_file(id):
    """
    file with game id
    :param id: game id
    :return: path to file
    """
    id_dir = "./siteCode/egames/"
    id_path = os.path.abspath(id_dir + "id_" + str(id))
    data = str(id) + "\n" + str(datetime.now())
    print data
    with file(id_path, "wb") as f:
        f.write(data)

    # add server adress, time

    return id_path


def create_new_blocker(user, game_id):
    """
    responsible for new blocker creation including db management
    :param user: user object
    :param game_id: game id
    :return: blocker path, the name of the game
    """
    print game_id
    games_dir = "./siteCode/games/"
    game_path = os.path.abspath(games_dir + str(game_id) + ".exe")
    ready_blocker = os.path.abspath(r".\siteCode\ready_blockers\\" + str(user.id) + str(game_id) + ".exe")
    # G:\cyber\Final_Cyber_Project\MileStones\Site\siteCode\ready_blockers
    # encrypt file
    e_dict = crypto.encrypt(game_path)

    # create GameDownloaded
    game = models.GameDownload(Crypto_key=e_dict["key"], Crypto_iv=e_dict["iv"], user_id=user.id, game_id=game_id)
    user.games_downloaded.append(game)
    db.session.flush()  # needed?
    # create id fie
    id_path = create_data_file(game.id)

    game_type = models.Game.query.filter_by(id=game_id).first()

    game_type.downloads = game_type.downloads + 1

    db.session.commit()  # ^

    # compile
    compile_blocker(ready_blocker, e_dict["encrypted_code_path"], id_path)

    # delete files
    os.remove(e_dict["encrypted_code_path"])
    os.remove(id_path)

    game_name = models.Game.query.filter_by(id=game_id).first().name
    print ready_blocker

    return ready_blocker, game_name
    # return download_and_remove(e_dict["encrypted_code_path"], filename)


def create_new_blocker_no_enc(user, game_id):
    """
    responsible for new blocker creation including db management no encryption
    :param user: user object
    :param game_id: game id
    :return: blocker path, the name of the game
    """
    games_dir = "./siteCode/games/"
    game_path = os.path.abspath(games_dir + str(game_id) + "noEnc.exe")
    ready_blocker = os.path.abspath(r".\siteCode\ready_blockers\\" + str(user.id) + str(game_id) + "noEnc.exe")
    # G:\cyber\Final_Cyber_Project\MileStones\Site\siteCode\ready_blockers
    # encrypt file
    e_dict = crypto.no_encryption(game_path)

    # create id fie
    id_path = create_data_file("-1")

    # compile
    compile_blocker(ready_blocker, e_dict["encrypted_code_path"], id_path)

    # delete files
    os.remove(e_dict["encrypted_code_path"])
    os.remove(id_path)
    return ready_blocker
    # return download_and_remove(e_dict["encrypted_code_path"], filename)
