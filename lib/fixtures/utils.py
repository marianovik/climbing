import requests as r

from lib.fixtures.data.links import IMAGES


def load_imgs():
    b_images = []
    for i in IMAGES:
        response = r.get(i)
        b_images.append(
            {
                "img": response.content,
                "name": "logo",
                "mimetype": response.headers["content-type"],
            }
        )
    return b_images
