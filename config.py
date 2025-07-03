import tomllib

FILE_NAME = "config.toml"
with open(FILE_NAME, "rb") as config_file:
    Config = tomllib.load(config_file)

if __name__ == "__main__":
    from json import dumps
    print(f"{FILE_NAME} loaded as:\n{dumps(Config, indent=4)}")
