# 🚀 FreeWorld Career Services Pathway Portal - Deployment Guide

## 🔒 Security & Environment Setup

### For Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
# Copy template and edit with your keys
cp .env.template .env
nano .env  # Add your actual API keys
```

3. **Create Supabase table:**
- Log into your Supabase dashboard
- Go to SQL Editor
- Run the SQL from `create_pathway_jobs_table.sql`

4. **Test local setup:**
```bash
python env_loader.py  # Check environment variables
streamlit run app.py  # Run locally
```

### For Streamlit Cloud Deployment

1. **Fork/Clone this repo to your GitHub**

2. **Create Streamlit Cloud app:**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub repo
- Select branch: `main`
- Main file path: `app.py`

3. **Configure secrets in Streamlit Cloud:**
- In your app dashboard, go to "Settings" → "Secrets"
- Copy contents from `.streamlit/secrets.toml.template`
- Replace with your actual API keys

4. **Deploy and test**

## 🗄️ Database Setup

### Supabase Table Creation

The pathway portal uses a separate `pathway_jobs` table to avoid conflicts with the main job scraper. Run this SQL in your Supabase dashboard:

```sql
-- See create_pathway_jobs_table.sql for complete schema
CREATE TABLE pathway_jobs (
    job_id text PRIMARY KEY,
    title text,
    company text,
    -- ... other fields
    career_pathway text,
    training_provided boolean DEFAULT false
    -- ... indexes and triggers
);
```

## 🔑 Required Environment Variables

### Core API Keys (Required)
- `OPENAI_API_KEY` - OpenAI API for job classification
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key

### Optional Integrations
- `AIRTABLE_API_KEY` - For CRM integration
- `AIRTABLE_BASE_ID` - Airtable base ID
- `AIRTABLE_TABLE_ID` - Airtable table ID
- `OUTSCRAPER_API_KEY` - For job scraping
- `SHORT_IO_API_KEY` - For link tracking

## 🚨 Security Checklist

### ✅ Before Going Public

- [ ] All API keys removed from code
- [ ] `.env` and `secrets.toml` in `.gitignore`
- [ ] No secrets in git history
- [ ] Separate Supabase table created
- [ ] Environment loader tested locally
- [ ] Streamlit Cloud secrets configured

### 🛡️ Security Features

1. **Environment Variable Protection:**
   - Local: `.env` files (git-ignored)
   - Cloud: Streamlit secrets
   - Fallback: OS environment variables

2. **Separate Database:**
   - Uses `pathway_jobs` table
   - Isolated from main job scraper data
   - Pathway-specific schema

3. **API Key Masking:**
   - Development tools mask sensitive data
   - No keys exposed in logs or UI

## 🧪 Testing

### Local Testing
```bash
# Test environment setup
python env_loader.py

# Test Streamlit app
streamlit run app.py

# Test with sample search
# Use "Memory Only" first (safer, cheaper)
```

### Production Testing
1. Deploy to Streamlit Cloud
2. Test memory-only searches first
3. Verify Supabase integration
4. Test PDF generation
5. Validate link tracking

## 📊 Monitoring

### Key Metrics to Watch
- API usage costs (OpenAI, Outscraper)
- Supabase database growth
- Search response times
- PDF generation success rates

### Logging
- Streamlit Cloud provides basic logs
- Monitor for API errors
- Watch for database connection issues

## 🔄 Updates & Maintenance

### Regular Tasks
- Monitor API quotas
- Clean old job data (7+ days)
- Update coach permissions
- Review classification accuracy

### Emergency Procedures
- Disable API calls: Set environment variables to empty
- Stop processing: Remove from Streamlit Cloud
- Database cleanup: Use Supabase dashboard

## 📞 Support

For deployment issues:
1. Check environment variables with `python env_loader.py`
2. Verify Supabase table exists
3. Check Streamlit Cloud logs
4. Ensure all required dependencies installed