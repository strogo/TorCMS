import config

from torcms.core.tool.send_email import send_mail

send_mail(['bukun@osgeo.cn'], 'title', 'This just test.')

def Test():
    assert True