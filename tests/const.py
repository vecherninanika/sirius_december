from conf.config import settings

API_PREFIX = settings.API_PREFIX

URLS = {
    "api": {
        "user": {
            "register": API_PREFIX + "/user/register",
            "login": API_PREFIX + "/user/login",
        },
        "user": {"user": API_PREFIX + "/user"},
        "ingredient": {"ingredient": API_PREFIX + "/ingredient"},
        "recipe": {"recipe": API_PREFIX + "/recipe"},
    }
}
