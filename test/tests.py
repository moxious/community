import os
import json

def reality_operational(x):
    return x == x

def test_reality_operational():
    assert reality_operational(100) == True

def get_media():
    import json
    with open(os.path.join(os.path.dirname(__file__), '../media.json')) as f:
        return json.load(f)

def test_media_well_formed():
    media = get_media()
    assert isinstance(media, list)

required_fields = ["title", "url", "summary", "type"]

for field in required_fields:
    def media_has_field(field):
        media = get_media()
        for m in media:
            print("Checking for %s in %s" % (field, json.dumps(m)))
            assert field in m
    test_name = f"test_media_all_have_{field}"
    globals()[test_name] = lambda: media_has_field(field)

