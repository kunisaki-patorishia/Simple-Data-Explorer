# Quick Railway Deployment Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy Backend

1. Go to [railway.app](https://railway.app) → New Project
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. **IMPORTANT: Set Root Directory to `backend`**
   - Go to Settings → Root Directory
   - Enter: `backend`
   - This tells Railway where to find the Dockerfile
5. **Add PostgreSQL**: New → Database → PostgreSQL
6. **Set Environment Variables**:
   ```
   ALLOWED_ORIGINS=https://your-frontend.railway.app
   FRONTEND_URL=https://your-frontend.railway.app
   ```
   (Update after deploying frontend)
7. Copy the backend URL (e.g., `https://your-backend.railway.app`)

### Step 3: Deploy Frontend

1. In same Railway project: New → GitHub Repo
2. **IMPORTANT: Set Root Directory to `frontend`**
   - Go to Settings → Root Directory
   - Enter: `frontend`
   - This tells Railway where to find the Dockerfile
3. **Set Environment Variable**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```
   (Use the backend URL from Step 2)
4. Copy the frontend URL

### Step 4: Update Backend CORS

1. Go to backend service → Variables
2. Update:
   ```
   ALLOWED_ORIGINS=https://your-frontend.railway.app
   FRONTEND_URL=https://your-frontend.railway.app
   ```
3. Railway auto-redeploys

### Step 5: Test!

Visit your frontend URL and test the app!

## Environment Variables Cheat Sheet

**Backend:**
- `DATABASE_URL` - Auto-set by Railway PostgreSQL
- `ALLOWED_ORIGINS` - Your frontend URL
- `FRONTEND_URL` - Your frontend URL
- `PORT` - Auto-set by Railway

**Frontend:**
- `NEXT_PUBLIC_API_URL` - Your backend URL
- `PORT` - Auto-set by Railway

## Troubleshooting

**CORS Errors?**
- Check `ALLOWED_ORIGINS` matches frontend URL exactly
- Include `https://` in URLs

**API Not Working?**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend logs in Railway dashboard

**Database Issues?**
- Ensure PostgreSQL service is added
- `DATABASE_URL` should be auto-set

## Need More Help?

See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) for detailed guide.

