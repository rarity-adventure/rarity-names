import base64
import json


def test_svg(n1, barb, barb2, owner):
    svg = n1.tokenURI(1)
    svg = svg.split(",")[1]
    b64_str = svg.encode('ascii')
    url_bytes_b64 = base64.urlsafe_b64decode(b64_str)
    str_64 = str(url_bytes_b64, "utf-8")
    j = json.loads(str_64)
    assert j['name'] == "Conan"
    assert 'description' in j
    assert 'image' in j
    image1 = j['image']

    n1.clear_summoner_name(barb, {'from': owner})
    svg = n1.tokenURI(1)
    svg = svg.split(",")[1]
    b64_str = svg.encode('ascii')
    url_bytes_b64 = base64.urlsafe_b64decode(b64_str)
    str_64 = str(url_bytes_b64, "utf-8")
    j = json.loads(str_64)
    assert j['name'] == "Conan"
    assert 'description' in j
    assert 'image' in j
    image2 = j['image']

    assert not image1 == image2
