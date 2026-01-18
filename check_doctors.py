import os
from supabase import create_client

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if url and key:
    supabase = create_client(url, key)
    result = supabase.table('doctors').select('id, name, email, department_id').execute()
    print(f'Total doctors: {len(result.data)}')
    if result.data:
        for i, doctor in enumerate(result.data[:5], 1):
            print(f'{i}. {doctor.get("name")} ({doctor.get("email")})')
    else:
        print('No doctors found in database!')
else:
    print('Missing Supabase credentials')
