import os
import re
import pytest
import requests

def load_env_local():
    env_vars = {}
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.local')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars

@pytest.fixture(scope="session")
def env_config():
    config = load_env_local()
    return config

@pytest.fixture(scope="session")
def frontend_url():
    return "http://localhost:5173"

@pytest.fixture(scope="session")
def supabase_url(env_config):
    url = env_config.get("VITE_SUPABASE_URL", "")
    return url.rstrip('/')

@pytest.fixture(scope="session")
def supabase_anon_key(env_config):
    return env_config.get("VITE_SUPABASE_PUBLISHABLE_KEY", "")

@pytest.fixture(scope="session")
def supabase_headers(supabase_anon_key):
    return {
        "apikey": supabase_anon_key,
        "Authorization": f"Bearer {supabase_anon_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

@pytest.fixture
def http_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "CCMS-IA3-Pytest-TestSuite/1.0"
    })
    return session

