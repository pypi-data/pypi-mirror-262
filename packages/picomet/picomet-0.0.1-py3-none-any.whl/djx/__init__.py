import json
from importlib import import_module

cache = {}


def call_action(request):
    action = request.headers.get("Action")
    if action:
        action_module, action_name = action.split(".")
        module = f"{action_module}.actions"
        if not cache.get(module):
            try:
                actions = import_module(module)
                if hasattr(actions, action_name):
                    payload = json.loads(request.headers.get("Payload", "{}"))
                    targets = getattr(actions, action_name)(request, payload)
                    for target in targets:
                        if target not in request.targets:
                            request.targets.append(target)
            except ModuleNotFoundError:
                pass
        else:
            actions = cache[module]
            if hasattr(actions, action_name):
                payload = json.loads(request.headers.get("Payload", "{}"))
                targets = getattr(actions, action_name)(request, payload)
                for target in targets:
                    if target not in request.targets:
                        request.targets.append(target)
