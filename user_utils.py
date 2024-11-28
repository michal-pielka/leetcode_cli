import json
import re
import os
import platform

def get_config_path():
    if platform.system() == "Windows":
        config_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
        config_path = os.path.join(config_dir, "leetcode", "config.json")

    else:  # macOS and Linux
        config_dir = os.path.expanduser("~/.config/leetcode")
        config_path = os.path.join(config_dir, "config.json")

    return config_path


def set_cookie(cookie):
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    # Create the config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Load existing config if it exists, else start with an empty dict
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Config file is corrupted. Overwriting it.")

    # Update the cookie value
    config["cookie"] = cookie

    # Save the updated config back to the file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Cookie saved to {config_path}")


def extract_csrf_token(cookie):
    match = re.search(r'csrftoken=([^;]+)', cookie)

    if match:
        return match.group(1)
    else:
        return None


def set_username(username):
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    # Create the config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Load existing config if it exists, else start with an empty dict
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Config file is corrupted. Overwriting it.")

    # Update the user_slug value
    config["username"] = username

    # Save the updated config back to the file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Username saved to {config_path}")


def load_cookie():
    config_path = get_config_path()

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("cookie")
        except (json.JSONDecodeError, KeyError):
            print("Error: Invalid config file format.")
            return None
    else:
        print("Error: Config file not found. Use 'save_cookie' to create one.")
        return None


# Example usage
if __name__ == "__main__":
    username = "BucketAbuser"
    cookie = '__stripe_mid=50af2006-33dc-414e-b857-14bc3e74ac84742cff; cf_clearance=kK.2EfoZktQ.kN9BwHEULRvqhpGRXgKzIkFlSsL_._8-1731354607-1.2.1.1-THHVDQhzyCa0xdOZr4Aj0VvK_NWcDlJqe7Y1JXr53eYiLfPwzy04n1zJVcin0cyYRUYGDxa_ul0UpEOfyGe3ndoJ3LDmj2z2Pp23.EeJhSRjpbq.W2tUNo8epGlY9adZT_y_s6qtqIykedkjVnd0FD6kJlEpxfdl7OaXeagxQw2K0a2DR5N1EKKTsA6F5Ql1TdEAT09JdUnz3supzh0xJ1VNSKrF.n5uHH_vdQFNV5cAZFf_.BDhEmIhJ7ZLzQDc7EMBFWrstNokCAv0dGix9SrTnsKdyquXYnG.MHq2.kynS0Ti3p8rQFDUydGW8akf0DTYh_xtW3_gBTLP1kod3lJ3gF7n6bDZb4Ep3DxSKuFzPct7LJh6jDVlcG.rct9ThQfhVpB8kiZ1qh5R6NyYWSVf7foqvPolqdCPvJWpAVaBW05IkbxfhjkZ1qEYVcNL; csrftoken=tKsgNsn78jkr8zPZEBlwQhfjLdCqjzdpUIOfvE4utfWkFIuBJNstG5fpoG9NakSY; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWKziVJmenljgmlRanFukpxepQbEIsABb7LkM:1tAaQK:tKp42SuG0Dl-oSPWsZ0BojMl2iTyREsyPB7hQ5STU1E; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNzIxNzc4NCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM1NDEwZGJkZTBhZmE2MjhhM2NhYjZkZmI1ZDViNjcyMmRmOTg5OTRmMGRkZjc5MmJhOTQ0Y2JmOGI2M2RmZGEiLCJpZCI6NzIxNzc4NCwiZW1haWwiOiJtcGllbGthNzI2QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiQnVja2V0QWJ1c2VyIiwidXNlcl9zbHVnIjoiQnVja2V0QWJ1c2VyIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2RlZmF1bHRfYXZhdGFyLmpwZyIsInJlZnJlc2hlZF9hdCI6MTczMjYxNjY0NCwiaXAiOiIxMDkuMjQzLjEuOTMiLCJpZGVudGl0eSI6ImE0NTVlYmM2N2QwYjUwMDdlMmEwNTU0MTRkZDE0ZDc4IiwiZGV2aWNlX3dpdGhfaXAiOlsiZDk5MzBhOGIxMTZhNzdkZGQzN2MyOGI2ZGI3MGIxNmQiLCIxMDkuMjQzLjEuOTMiXSwic2Vzc2lvbl9pZCI6MTgwNjEzLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.FHPzMW1NFOnELXXcHzB3WIUGJOSs7Woh36JuYlqsvR0; ip_check=(false, "109.243.1.93"); INGRESSCOOKIE=6542b644a233f3d8a33703e8cfe82090|8e0876c7c1464cc0ac96bc2edceabd27; __cf_bm=a45.X5vniCgYusorKY77Z18pSrW5BX0iZ2jOZi15bso-1732626577-1.0.1.1-5ulEYk_3r.mq7KsUDVCejAs7MqaVvdBYNSrv6tqReVInEcFT45iLSVadbq_dA9Us_w9w_B6dsi88.yPjqYo9Zw'

    set_cookie(cookie)
    set_username(username)
