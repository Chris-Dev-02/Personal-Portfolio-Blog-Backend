import os
import sys

def get_env(var_name, cast=str, default=None, required=True):
    raw_value = os.getenv(var_name, default)

    if raw_value is None and required:
        print(f"ERROR: missing environment variable '{var_name}' and no default value provided.")
        sys.exit(1)

    try:
        if cast is bool:
            return str(raw_value).lower() in ['1', 'true', 'yes']
        return cast(raw_value)
    except Exception as e:
        print(f"ERROR: failed to convert '{var_name}'='{raw_value}' to {cast}: {e}")
        sys.exit(1)

def get_env_list(var_name, default=None, required=False, separator=","):
    raw_value = os.getenv(var_name)

    if raw_value is None:
        if required and default is None:
            print(f"ERROR: missing environment variable '{var_name}' and no default value provided.")
            sys.exit(1)
        return default or []

    return [item.strip() for item in raw_value.split(separator) if item.strip()]