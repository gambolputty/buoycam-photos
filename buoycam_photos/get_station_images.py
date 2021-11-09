from typing import List, Literal, Tuple, Union
import requests
from io import BytesIO
from PIL import Image, ImageStat

"""
To view the most recent BuoyCAM image from an NDBC station, use this URL:
https://www.ndbc.noaa.gov/buoycam.php?station=xxxxx

Source: https://www.ndbc.noaa.gov/buoycamlinks.shtml

All cams: https://www.ndbc.noaa.gov/buoycams.shtml

"""

DEBUG = False


def get_cam_photo(station_name: str) -> Image:
    station_image_url = f'https://www.ndbc.noaa.gov/buoycam.php?station={station_name}'
    response = requests.get(station_image_url)
    return Image.open(BytesIO(response.content))


def get_image_brigthness(img: Image) -> int:
    # Source: https://newbedev.com/what-are-some-methods-to-analyze-image-brightness-using-python
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


def crop_cam_photo(img: Image):
    """
    Crop image into six pieces.
    Exclude lower black border and images that are too dark.
    """
    result = []
    width = 480
    height = 270
    all_boxes = [
        # (left, upper, right, lower)
        (0, 0, width, height),
        (width+1, 0, width*2, height),
        (width*2+1, 0, width*3, height),
        (width*3+1, 0, width*4, height),
        (width*4+1, 0, width*5, height),
        (width*5+1, 0, width*6, height),
    ]

    for index, box in enumerate(all_boxes):
        new_img = img.crop(box)
        brightness = get_image_brigthness(new_img)

        if DEBUG:
            print(f'{index}, {brightness}')

        if brightness > 180:
            # image is too bright
            continue
        elif brightness < 75:
            # image is too dark
            continue

        result.append(new_img)

    return result


def get_station_images(name: str, scale: Union[None, Tuple[int, int]] = (540, 304)):
    img = get_cam_photo(name)
    cropped_images = crop_cam_photo(img)

    if scale:
        result = [new_img.resize(scale, Image.ANTIALIAS) for new_img in cropped_images]
    else:
        result = cropped_images

    if DEBUG:
        img.save(f'./buoycam_photos/test.jpg')
        for index, new_img in enumerate(result):
            new_img.save(f'./buoycam_photos/test_{index}.jpg')

    return result


if __name__ == '__main__':
    get_station_images('42035')
