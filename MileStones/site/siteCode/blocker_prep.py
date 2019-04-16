import subprocess, os, time
from siteCode import crypto, models, db
import commands

decryptor_path = os.path.abspath(r".\siteCode\ready_blockers\decryptor.cs")
decryptor_no_enc_path = os.path.abspath(r"./siteCode/ready_blockers/decryptor_noenc.cs")




def compile_blocker(blocker_path, e_game_path, id_path):
    if os.environ['COMPUTERNAME']=='DESKTOP-NDHRRRG':
        ces_path = r'"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\Roslyn\csc.exe"'#home
    else:
        ces_path = r'"C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn\csc.exe"' #cyber
    new_file = blocker_path
    code_file = e_game_path
    id_file = id_path
    blocker_code_file = decryptor_path
    rec_pat = "C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\Common7\IDE\Extensions\Xamarin.VisualStudio\Xamarin.Inspector.Windows\Client"
    command = ces_path + \
              " /out:" + new_file + \
              " /res:" + code_file + ",code,private  " + " /res:" + id_file + ",id,private " + \
              "/reference:System.Net.Http.dll /reference:System.Security.Cryptography.Primitives.dll " + \
              blocker_code_file
    """
    home:
    "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\Roslyn\csc.exe"
    school:
    "C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn\csc.exe"
    
    
    doxomintation:
    https://docs.microsoft.com/en-us/previous-versions/ms379563(v=vs.80)
    """

    try:
        x = subprocess.call(command, shell=False)
    except Exception as e:
        print "there was a compilation error"
        print "massage: ", e.message
        print "comand: ", command


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
    ready_blocker = os.path.abspath(r".\siteCode\ready_blockers\\" + str(user.id) + str(game_id) + ".exe")
    # G:\cyber\Final_Cyber_Project\MileStones\Site\siteCode\ready_blockers
    # encrypt file
    e_dict = crypto.encrypt(game_path)

    # create GameDownloaded
    game = models.GameDownload(Crypto_key=e_dict["key"], Crypto_iv=e_dict["iv"], user_id=user.id,game_id=game_id)
    user.games_downloaded.append(game)
    db.session.flush()  # needed?

    # create id fie
    id_path = create_id_file(game.id)

    db.session.commit()  # ^

    # compile
    compile_blocker(ready_blocker, e_dict["encrypted_code_path"], id_path)

    # delete files
    os.remove(e_dict["encrypted_code_path"])
    os.remove(id_path)
    return ready_blocker
    # return download_and_remove(e_dict["encrypted_code_path"], filename)


def create_new_blocker_no_enc(user, game_id):
    games_dir = "./siteCode/games/"
    game_path = os.path.abspath(games_dir + str(game_id) + ".exe")
    ready_blocker = os.path.abspath(r".\siteCode\ready_blockers\\" + str(user.id) + str(game_id) + ".exe")
    # G:\cyber\Final_Cyber_Project\MileStones\Site\siteCode\ready_blockers
    # encrypt file
    e_dict = crypto.no_encryption(game_path)

    # create GameDownloaded
    game = models.GameDownload(Crypto_key=e_dict["key"], Crypto_iv=e_dict["iv"], user_id=user.id)
    user.games_downloaded.append(game)
    db.session.flush()  # needed?

    # create id fie
    id_path = create_id_file(game.id)

    db.session.commit()  # ^

    # compile
    compile_blocker(ready_blocker, e_dict["encrypted_code_path"], id_path)

    # delete files
    os.remove(e_dict["encrypted_code_path"])
    os.remove(id_path)
    return ready_blocker
    # return download_and_remove(e_dict["encrypted_code_path"], filename)


