from torcms.model.user_model import MUser

def create_admin():
    uu = MUser()
    post_data = {
        'user_name': ['giser'],
        'user_pass': ['g131322'],
        'user_email': ['name@qkq.com'],
        'privilege': ['fffff'],
    }

    # tt = uu.insert_data(post_data)
    # print(tt)