import dacite
import os
import tomllib


class Configuration:
    cache_dir: str = f"{os.environ["HOME"]}/.cache/git2know"
    home_dir: str = os.environ["HOME"]

converters = {
    str: str,
}

def load_config() -> Configuration:
    raw_cfg = dict({})
    for location in [
        f"{os.getcwd()}/.git2know.toml",
        f"{os.environ["HOME"]}/.config/git2know/config.toml",
    ]:
        try:
            raw_cfg = tomllib.load(location)
            print(f"Loaded config from {location}")
            break
        except FileNotFoundError:
            pass
    config = dacite.from_dict(
        config=dacite.Config(type_hooks=converters),
        data_class=Configuration,
        data=raw_cfg,
    )
    print(f"Config: {config}")
    return config
