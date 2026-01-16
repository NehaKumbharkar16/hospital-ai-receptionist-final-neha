import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = None  # Anon key client for read operations
supabase_admin: Client = None  # Service role client for writes (bypasses RLS)

async def init_db():
    global supabase, supabase_admin
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Connected to Supabase with anon key")
    else:
        print("Warning: Supabase anon key not found")
    
    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
        supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        print("Connected to Supabase with service role key")
    else:
        print("Warning: Supabase service role key not found")

def get_supabase() -> Client:
    return supabase

def get_supabase_admin() -> Client:
    return supabase_admin