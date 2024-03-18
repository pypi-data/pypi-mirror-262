import json
from comfy_ui_client.client import ComfyUIClient
from comfy_ui_client.type import ImageRef


def test_text2img():
    client = ComfyUIClient("localhost:8188")
    with open("text2img.json", "r") as f:
        prompt_text = f.read()

    prompt = json.loads(prompt_text)
    ret = client.get_outputs(prompt)
    assert "images" in ret


def test_img2img():
    client = ComfyUIClient("localhost:8188")
    with open("img2img.json", "r") as f:
        prompt_text = f.read()

    client.upload_image(ImageRef(filename="example.png", subfolder="", type="input"), "./example.png")

    prompt = json.loads(prompt_text)
    ret = client.get_outputs(prompt)
    assert "images" in ret


def test_get_history():
    client = ComfyUIClient("localhost:8188")
    history = client.get_history(None)
    assert history is not None


def test_clear_history():
    client = ComfyUIClient("localhost:8188")
    client.clear_history()


def test_delete_history():
    client = ComfyUIClient("localhost:8188")
    history = client.get_history(None)
    client.delete_history(list(history.keys()))


