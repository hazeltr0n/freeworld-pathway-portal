-- Add missing columns to pathway_jobs table
-- These columns are referenced in the code but missing from the table schema

-- Add classified_at column
ALTER TABLE pathway_jobs
ADD COLUMN IF NOT EXISTS classified_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL;

-- Add apply_url column
ALTER TABLE pathway_jobs
ADD COLUMN IF NOT EXISTS apply_url text;

-- Create index for classified_at for performance
CREATE INDEX IF NOT EXISTS idx_pathway_jobs_classified_at ON pathway_jobs(classified_at);

-- Update any existing rows to have classified_at = created_at
UPDATE pathway_jobs
SET classified_at = created_at
WHERE classified_at IS NULL;

-- Confirm the changes
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'pathway_jobs'
AND column_name IN ('classified_at', 'apply_url')
ORDER BY column_name;