-- Create pathway_jobs table for Career Services Pathway Portal
-- This is a separate table from the main jobs table to avoid conflicts

CREATE TABLE pathway_jobs (
    job_id text PRIMARY KEY,
    title text,
    company text,
    description text,
    location text,
    salary text,
    posted_date timestamp with time zone,
    source text,
    url text,

    -- AI Classification fields
    match text,
    reason text,
    summary text,
    route_type text,
    fair_chance text,
    endorsements text,
    career_pathway text,
    training_provided boolean DEFAULT false,

    -- Business rules
    is_owner_op boolean DEFAULT false,
    is_school_bus boolean DEFAULT false,
    is_spam_source boolean DEFAULT false,

    -- Metadata
    market text,
    coach text,
    coach_username text,
    candidate_id text,
    candidate_name text,

    -- System fields
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    classified_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    final_status text,
    is_fresh_job boolean DEFAULT true,

    -- Link tracking
    tracked_url text,
    link_id text,
    tags text,
    apply_url text
);

-- Create indexes for performance
CREATE INDEX idx_pathway_jobs_market ON pathway_jobs(market);
CREATE INDEX idx_pathway_jobs_match ON pathway_jobs(match);
CREATE INDEX idx_pathway_jobs_route_type ON pathway_jobs(route_type);
CREATE INDEX idx_pathway_jobs_created_at ON pathway_jobs(created_at);
CREATE INDEX idx_pathway_jobs_coach ON pathway_jobs(coach);
CREATE INDEX idx_pathway_jobs_final_status ON pathway_jobs(final_status);
CREATE INDEX idx_pathway_jobs_career_pathway ON pathway_jobs(career_pathway);
CREATE INDEX idx_pathway_jobs_fair_chance ON pathway_jobs(fair_chance);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_pathway_jobs_updated_at BEFORE UPDATE ON pathway_jobs FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Enable Row Level Security (optional)
-- ALTER TABLE pathway_jobs ENABLE ROW LEVEL SECURITY;