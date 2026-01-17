-- Add columns to chat_sessions table to store patient consultation data
ALTER TABLE chat_sessions 
ADD COLUMN IF NOT EXISTS patient_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS patient_age INTEGER,
ADD COLUMN IF NOT EXISTS symptoms TEXT,
ADD COLUMN IF NOT EXISTS suggested_ward VARCHAR(50);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_chat_sessions_patient_name ON chat_sessions(patient_name);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_ward ON chat_sessions(suggested_ward);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created ON chat_sessions(created_at);
