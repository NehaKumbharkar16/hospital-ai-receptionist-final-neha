-- Fix the chat_sessions table column sizes
ALTER TABLE chat_sessions 
ALTER COLUMN status TYPE VARCHAR(50);

-- Increase patient_name size for longer names
ALTER TABLE chat_sessions 
ALTER COLUMN patient_name TYPE VARCHAR(500);

-- Increase suggested_ward size
ALTER TABLE chat_sessions 
ALTER COLUMN suggested_ward TYPE VARCHAR(50);
