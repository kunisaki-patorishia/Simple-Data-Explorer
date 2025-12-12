# Railway Deployment Guide

This guide will help you deploy the Simple Data Explorer application to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Push your code to GitHub (Railway connects via GitHub)
3. **Railway CLI** (Optional): Install for easier management
   ```bash
   npm i -g @railway/cli
   ```

## Deployment Steps

### Option 1: Deploy via Railway Dashboard (Recommended)

#### Step 1: Deploy Backend

1. **Create New Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Add Backend Service**
   - Click "New" → "GitHub Repo"
   - Select your repository
   - **CRITICAL: Before deploying, go to Settings**
   - **Set Root Directory to: `backend`** (exactly, lowercase, no slash)
   - Railway will now find `backend/Dockerfile`
   - **Build Type**: Should auto-detect as "Dockerfile" (if not, set it manually)

3. **Configure Backend**
   - **Root Directory**: `backend` (must be set!)
   - **Build Command**: (Auto-detected from Dockerfile)
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Save settings**

4. **Add PostgreSQL Database** (Optional but Recommended)
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set `DATABASE_URL` environment variable
   - Your app will automatically use PostgreSQL instead of SQLite

5. **Set Environment Variables**
   - Go to backend service → Variables tab
   - Add the following:
     ```
     ALLOWED_ORIGINS=https://your-frontend-url.railway.app
     FRONTEND_URL=https://your-frontend-url.railway.app
     ```
   - Note: You'll update `FRONTEND_URL` after deploying the frontend

6. **Deploy**
   - Railway will automatically build and deploy
   - Note the backend URL (e.g., `https://your-backend.railway.app`)

#### Step 2: Deploy Frontend

1. **Add Frontend Service**
   - In the same Railway project, click "New" → "GitHub Repo"
   - Select the same repository
   - **CRITICAL: Before deploying, go to Settings**
   - **Set Root Directory to: `frontend`** (exactly, lowercase, no slash)
   - Railway will now find `frontend/Dockerfile`
   - **Build Type**: Should auto-detect as "Dockerfile" (if not, set it manually)

2. **Configure Frontend**
   - **Root Directory**: `frontend` (must be set!)
   - **Build Command**: (Auto-detected from Dockerfile)
   - **Start Command**: `node server.js`
   - **Save settings**

3. **Set Environment Variables**
   - Go to frontend service → Variables tab
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app
     ```
   - Replace with your actual backend URL from Step 1

4. **Update Backend CORS**
   - Go back to backend service → Variables
   - Update `FRONTEND_URL` and `ALLOWED_ORIGINS` with your frontend URL:
     ```
     ALLOWED_ORIGINS=https://your-frontend.railway.app
     FRONTEND_URL=https://your-frontend.railway.app
     ```
   - Railway will automatically redeploy

5. **Deploy**
   - Railway will build and deploy the frontend
   - Your app will be live!

### Option 2: Deploy via Railway CLI

1. **Login to Railway**
   ```bash
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   ```

3. **Link to Existing Project** (if you created one in dashboard)
   ```bash
   railway link
   ```

4. **Deploy Backend**
   ```bash
   cd backend
   railway up
   ```

5. **Set Environment Variables**
   ```bash
   railway variables set ALLOWED_ORIGINS=https://your-frontend.railway.app
   railway variables set FRONTEND_URL=https://your-frontend.railway.app
   ```

6. **Deploy Frontend**
   ```bash
   cd ../frontend
   railway up
   railway variables set NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```

## Environment Variables Reference

### Backend Service

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Railway) | `postgresql://user:pass@host:port/db` |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | `https://app.railway.app,https://localhost:3000` |
| `FRONTEND_URL` | Frontend URL for CORS | `https://your-frontend.railway.app` |
| `PORT` | Server port (auto-set by Railway) | `8000` |

### Frontend Service

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-backend.railway.app` |
| `PORT` | Server port (auto-set by Railway) | `3000` |

## Database Setup

### Using PostgreSQL (Recommended for Production)

Railway automatically provides a PostgreSQL database:
1. Add PostgreSQL service in Railway
2. Railway sets `DATABASE_URL` automatically
3. Your app will use PostgreSQL instead of SQLite
4. Database persists across deployments

### Using SQLite (Development Only)

If you don't add PostgreSQL:
- App will use SQLite
- **Warning**: SQLite files are ephemeral in Railway
- Data will be lost on redeploy
- Use PostgreSQL for production!

## Custom Domains

1. Go to your service → Settings → Domains
2. Click "Generate Domain" or "Custom Domain"
3. Railway provides free `.railway.app` domains
4. Update environment variables with new domain

## Monitoring & Logs

- **View Logs**: Service → Deployments → Click deployment → View logs
- **Metrics**: Service → Metrics tab
- **Health Check**: Visit `https://your-backend.railway.app/health/`

## Troubleshooting

### Backend Issues

**Problem**: CORS errors
- **Solution**: Check `ALLOWED_ORIGINS` and `FRONTEND_URL` match your frontend URL exactly

**Problem**: Database connection errors
- **Solution**: Ensure PostgreSQL service is added and `DATABASE_URL` is set

**Problem**: Port binding errors
- **Solution**: Use `$PORT` environment variable (Railway sets this automatically)

### Frontend Issues

**Problem**: API calls fail
- **Solution**: Verify `NEXT_PUBLIC_API_URL` is set correctly
- **Solution**: Check backend CORS settings include frontend URL

**Problem**: Build fails
- **Solution**: Check Dockerfile is correct
- **Solution**: Ensure `output: 'standalone'` is in `next.config.js`

**Problem**: 404 errors
- **Solution**: Ensure Next.js standalone output is configured correctly

## Post-Deployment Checklist

- [ ] Backend health check works: `https://your-backend.railway.app/health/`
- [ ] Frontend loads: `https://your-frontend.railway.app`
- [ ] API calls work from frontend
- [ ] Database seeding works (click "Seed Database" button)
- [ ] Search, filter, sort, pagination all work
- [ ] CORS is configured correctly (no CORS errors in browser console)
- [ ] Environment variables are set correctly

## Updating Your Deployment

1. **Push changes to GitHub**
2. Railway automatically detects changes
3. Railway rebuilds and redeploys
4. Check deployment logs for any issues

## Cost Considerations

- **Free Tier**: Railway offers a free tier with $5 credit/month
- **PostgreSQL**: Included in free tier (with limits)
- **Custom Domains**: Free `.railway.app` domains included
- **Usage**: Monitor usage in Railway dashboard

## Security Notes

1. **Environment Variables**: Never commit secrets to GitHub
2. **CORS**: Only allow trusted origins
3. **Database**: Use PostgreSQL in production (more secure than SQLite)
4. **HTTPS**: Railway provides HTTPS automatically

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## Quick Deploy Commands

```bash
# Backend
cd backend
railway up
railway variables set ALLOWED_ORIGINS=https://your-frontend.railway.app

# Frontend  
cd frontend
railway up
railway variables set NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

Happy Deploying! 🚀

