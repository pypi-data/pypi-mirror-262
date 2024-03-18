import json


# https://github.com/andreyryabtsev/comfyui-python-api/blob/main/comfyui_utils/comfy.py#L35
def _parse_queue(queue_json):
    """Returns a list of prompt IDs in the queue, the 0th (if present) element is currently executed."""
    assert len(queue_json["queue_running"]) <= 1
    result = []
    if queue_json["queue_running"]:
        result.append(queue_json["queue_running"][0][1])
    for pending in queue_json["queue_pending"]:
        result.append(pending[1])
    return result


def _find_prompt_in_history(history, prompt):
    for prompt_id, data in history.items():
        original_prompt = data["prompt"][2]
        if original_prompt == prompt:
            return prompt_id
    return None

