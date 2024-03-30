import requests

pic_url="https://miro.medium.com/v2/resize:fit:1400/1*NE9GCZliWRPy9km6Kmaarw.png"
#https://unsplash.com/photos/the-sun-is-setting-over-the-mountains-and-trees-KqHGlo04ELc

with open('pic1.jpg', 'wb') as handle:
    response = requests.get(pic_url, stream=True)

    if not response.ok:
        print(response)

    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)