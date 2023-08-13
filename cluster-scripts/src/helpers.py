from PIL import Image
import datetime


def save_optimized_image(file_names: list[str]):
    try:
        with Image.open(file_names[0]) as im:
            im_width, im_height = im.size
            im_resize = im.resize((im_width // 3, im_height // 3))

            im_rgb = im_resize.convert('RGB')
            im_rgb.save(f"{file_names[1]}", optimize=True, quality=70)
            im_rgb.save(f"{file_names[2]}", optimize=True, quality=70)
    except OSError as e:
        print(e)
        pass

def validate_time(x: str):
    try:
        now = datetime.datetime.utcnow()
        x_time = datetime.datetime.strptime(x[4:14], '%Y%m%d%H')

        if x_time >= now - datetime.timedelta(hours=24) and x_time <= now:
            return True
    except:
        pass
    return False
