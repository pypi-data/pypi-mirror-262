import json

import numpy as np
import pandas as pd
import requests

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class ApiRest:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# APIREST")
        method: str = settings["method"] if "method" in settings and settings["method"] else None
        url: str = settings["url"] if "url" in settings and settings["url"] else None
        headers: list = settings["headers"] if "headers" in settings and settings["headers"] else []
        params: list = settings["params"] if "params" in settings and settings["params"] else []

        if not method:
            msg = app_message["nodes"]["api-rest"]["no_method"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if not url:
            msg = app_message["nodes"]["api-rest"]["no_url"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            # method = "GET"
            # url = "https://api.clay.cl/v1/cuentas_bancarias/movimientos/"

            headers = json.dumps(headers)
            params = json.dumps(params)
            
            print(headers)
            
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
            )

            script.append(
                f"import requests\n\nresponse = requests.request(\n'{method}',\n'{url}',\nheaders={headers},\nparams={params}\n)"
            )

            response = response.json()

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(e.args)})")
        
        df = pd.DataFrame()

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
