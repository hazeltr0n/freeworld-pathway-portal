"""
Environment Variable Loader for FreeWorld Career Services Pathway Portal
Handles both local .env files and Streamlit Cloud secrets
"""

import os
from typing import Optional

def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable from either Streamlit secrets or .env file

    Priority:
    1. Streamlit secrets (st.secrets)
    2. Environment variables (.env via python-dotenv)
    3. OS environment variables
    4. Default value

    Args:
        key: Environment variable name
        default: Default value if not found

    Returns:
        Environment variable value or default
    """

    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except ImportError:
        pass
    except Exception:
        pass

    # Try loading from .env file (for local development)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Get from environment variables
    value = os.getenv(key, default)

    if value is None:
        raise ValueError(f"Environment variable '{key}' not found. Please check your .env file or Streamlit secrets.")

    return value

def check_required_env_vars() -> bool:
    """
    Check that all required environment variables are present

    Returns:
        True if all required vars are present, False otherwise
    """
    required_vars = [
        'OPENAI_API_KEY',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY'
    ]

    missing_vars = []

    for var in required_vars:
        try:
            get_env_var(var)
        except ValueError:
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📝 Please check your .env file or Streamlit secrets configuration")
        return False

    print("✅ All required environment variables are present")
    return True

def get_all_env_vars() -> dict:
    """
    Get all environment variables for the application

    Returns:
        Dictionary of all environment variables
    """

    env_vars = {
        # Required
        'OPENAI_API_KEY': get_env_var('OPENAI_API_KEY'),
        'SUPABASE_URL': get_env_var('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': get_env_var('SUPABASE_ANON_KEY'),

        # Optional
        'AIRTABLE_API_KEY': get_env_var('AIRTABLE_API_KEY'),
        'AIRTABLE_BASE_ID': get_env_var('AIRTABLE_BASE_ID'),
        'AIRTABLE_TABLE_ID': get_env_var('AIRTABLE_TABLE_ID'),
        'OUTSCRAPER_API_KEY': get_env_var('OUTSCRAPER_API_KEY'),
        'SHORT_IO_API_KEY': get_env_var('SHORT_IO_API_KEY'),

        # Development
        'DEBUG': get_env_var('DEBUG', 'False'),
        'APP_VERSION': get_env_var('APP_VERSION', 'v2.3'),
        'PIPELINE_VERSION': get_env_var('PIPELINE_VERSION', 'v3'),
    }

    return env_vars

if __name__ == "__main__":
    print("🔍 Environment Variable Check")
    print("=" * 40)

    if check_required_env_vars():
        env_vars = get_all_env_vars()
        print("\n📋 Environment Variables:")
        for key, value in env_vars.items():
            if value and 'key' in key.lower():
                # Mask API keys for security
                masked_value = value[:8] + '*' * (len(value) - 12) + value[-4:] if len(value) > 12 else '***masked***'
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}")
    else:
        print("\n❌ Environment setup incomplete")
        print("Please run: cp .env.template .env")
        print("Then edit .env with your actual API keys")