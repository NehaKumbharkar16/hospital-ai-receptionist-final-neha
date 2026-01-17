import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load from .env file (for local development)
load_dotenv()

# Get credentials from environment (works on Render, Docker, etc.)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = None  # Anon key client for read operations
supabase_admin: Client = None  # Service role client for writes (bypasses RLS)

async def init_db():
    global supabase, supabase_admin
    
    # Debug output
    print("\n[DATABASE] Initializing Supabase connection...")
    print(f"[DATABASE] URL: {SUPABASE_URL}")
    print(f"[DATABASE] Anon key present: {bool(SUPABASE_KEY)}")
    print(f"[DATABASE] Service role key present: {bool(SUPABASE_SERVICE_ROLE_KEY)}")
    
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[DATABASE] ✅ Connected with anon key (read operations)")
    else:
        print("[DATABASE] ❌ Anon key not found - reads may fail")
    
    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
        supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        print("[DATABASE] ✅ Connected with service role key (write operations)")
    else:
        print("[DATABASE] ❌ SERVICE ROLE KEY NOT FOUND - WRITES WILL FAIL")
        print("[DATABASE] Set SUPABASE_SERVICE_ROLE_KEY environment variable!")

def get_supabase() -> Client:
    return supabase

def get_supabase_admin() -> Client:
    return supabase_admin