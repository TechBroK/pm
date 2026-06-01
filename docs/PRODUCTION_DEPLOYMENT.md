# Production Deployment Checklist & Guide

## Pre-Deployment Checklist

### ✅ Security

- [x] CORS restricted to specific domains (not `["*"]`)
- [x] `.env` added to `.gitignore` (never commit secrets)
- [x] `.env.example` created for reference
- [x] API keys stored in environment variables only
- [x] No hardcoded credentials in code

### ✅ Configuration

- [x] Environment variables for dev/prod modes
- [x] Conditional seeding based on environment
- [x] Proper error logging with timestamps
- [x] Health check endpoint `/health` ready
- [x] Database initialization on startup

### ✅ Excluded from Deployment

- [x] Test files (test*\*.py, debug*\*.py)
- [x] Development files (.env is local only)
- [x] Documentation files (README, docs/)
- [x] Node modules and Python venv
- [x] Cache and build artifacts

### ✅ Production Ready

- [x] Dockerfile with health check
- [x] Docker image optimized (no cache, Python flags set)
- [x] Frontend pre-built and included
- [x] Structured logging configured
- [x] Error handling for missing assets

---

## Deployment Steps

### **Option 1: Railway (Recommended - Easiest)**

1. **Push code to GitHub**

   ```bash
   git add .
   git commit -m "Production deployment ready"
   git push origin main
   ```

2. **Create Railway project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

3. **Set environment variables**
   - In Railway dashboard: Variables tab
   - Add these variables:
     ```
     ENVIRONMENT=production
     OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
     ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
     SEED_ON_STARTUP=false
     ```

4. **Deploy**
   - Railway auto-detects Dockerfile
   - Builds and deploys automatically
   - Get public URL

### **Option 2: Render.com**

1. **Connect GitHub** → [render.com](https://render.com)

2. **Create Web Service**
   - Connect repo
   - Build command: (auto-detected from Dockerfile)
   - Start command: (auto-detected from Dockerfile)

3. **Add environment variables**
   - Same as Railway above

4. **Deploy** → Get URL

### **Option 3: Docker Compose (Self-Hosted)**

1. **On your server (VPS, EC2, DigitalOcean)**

   ```bash
   # Clone repo
   git clone https://github.com/your-org/pm.git
   cd pm
   ```

2. **Create production `.env`**

   ```bash
   cat > .env << EOF
   ENVIRONMENT=production
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
   ALLOWED_ORIGINS=https://yourdomain.com
   SEED_ON_STARTUP=false
   EOF
   ```

3. **Build and run**

   ```bash
   docker-compose up -d
   ```

4. **Set up reverse proxy** (Nginx/Apache)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

---

## Environment Variables Reference

| Variable             | Example                  | Description                                          |
| -------------------- | ------------------------ | ---------------------------------------------------- |
| `ENVIRONMENT`        | `production`             | Set to "production" for deployment                   |
| `OPENROUTER_API_KEY` | `sk-or-v1-...`           | Get from [openrouter.ai](https://openrouter.ai/keys) |
| `ALLOWED_ORIGINS`    | `https://yourdomain.com` | Comma-separated list of allowed domains              |
| `SEED_ON_STARTUP`    | `false`                  | Don't recreate demo data on each restart             |
| `DATABASE_URL`       | `sqlite:///kanban.db`    | Path to SQLite database                              |

---

## Post-Deployment Verification

1. **Health check**

   ```bash
   curl https://yourdomain.com/health
   # Should return: {"status":"ok"}
   ```

2. **Login**
   - Navigate to `https://yourdomain.com`
   - Login with: `user` / `password`

3. **AI integration**
   - Click "Ask AI" sidebar
   - Should connect to OpenRouter successfully

4. **Database persistence**
   - Add a card
   - Restart application
   - Card should still exist

---

## Database Backups (SQLite)

Since SQLite stores data in a single file:

```bash
# Backup from container
docker cp <container-id>:/app/backend/kanban.db ./backup-$(date +%Y%m%d).db

# Set up automated backup (cron job)
0 2 * * * docker cp pm_pm_1:/app/backend/kanban.db /backups/kanban-$(date +\%Y\%m\%d).db
```

---

## Monitoring

### Check logs

```bash
# Docker
docker logs -f <container-id>

# Systemd (if using systemd)
journalctl -u pm -f
```

### Key log patterns

```
"Database initialized successfully" → DB ready
"Successfully mounted frontend" → Frontend loaded
"Production mode: CORS allowed for" → CORS configured
"ERROR" → Issues to investigate
```

---

## Troubleshooting

| Issue                   | Solution                                                    |
| ----------------------- | ----------------------------------------------------------- |
| 404 on root `/`         | Frontend not built. Run `npm run build` before Docker build |
| API key not working     | Check `OPENROUTER_API_KEY` in environment variables         |
| CORS errors             | Update `ALLOWED_ORIGINS` to match your domain               |
| Database not persisting | Ensure Docker volume is mounted for `/app/backend/`         |
| Seed data missing       | Set `SEED_ON_STARTUP=true` first time only                  |

---

## Security Notes

1. **Never commit `.env`** - Only `.env.example` is committed
2. **Use HTTPS** - All production domains should use TLS/SSL
3. **Rotate API keys** - Regularly change OpenRouter API key
4. **Restrict CORS** - Never use `["*"]` in production
5. **Monitor logs** - Check for unauthorized access attempts
6. **Backup database** - SQLite file contains all user data

---

## Next Steps for MongoDB Migration

When ready to migrate to MongoDB:

1. Update `backend/db.py` to use `pymongo` instead of `sqlite3`
2. Add `pymongo` and `motor` to `requirements.txt`
3. Update `DATABASE_URL` to MongoDB connection string
4. Update seeding logic for MongoDB documents
5. Deploy with new environment variable pointing to MongoDB Atlas

For now, SQLite is perfect for MVP deployment.
