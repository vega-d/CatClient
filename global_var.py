from service_func import getDefaultHome 
# <==> ----- ----- ----- <==>
host = '0.0.0.0'
port = 80

quick_src = r''
no_image = r'static/img/no_image.jpg'
debug = True
url_path_separation = ';;'

home_folder = getDefaultHome()

# <==> ----- ----- ----- <==>
formats = {
    'vid': ['mp4', 'avi'],
    'pic': ['png', 'jpg', 'jpeg', 'gif'],
    'aud': ['mp3', 'ogg']
}
# <==> ----- ----- ----- <==>
