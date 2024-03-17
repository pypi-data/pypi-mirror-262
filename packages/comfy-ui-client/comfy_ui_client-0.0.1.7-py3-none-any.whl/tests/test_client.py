import json

from comfy_ui_client.client import ComfyUIClient


def test_text2img():
    client = ComfyUIClient("localhost:8188")
    with open("text2img.json", "r") as f:
        prompt_text = f.read()

    prompt = json.loads(prompt_text)
    ret = client.get_outputs(prompt)
    assert "images" in ret

