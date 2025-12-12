# Critical Fix: Railway Root Directory Not Set

## The Error You're Seeing

```
skipping 'Dockerfile' at 'backend/Dockerfile' as it is not rooted at a valid path (root_dir=, ...)
```

This means Railway's `root_dir` is **empty** - it doesn't know where to look for your Dockerfile.

## Solution: Set Root Directory in Railway Dashboard

### Step-by-Step Instructions

#### For Backend Service:

1. **Go to Railway Dashboard** → Your Project
2. **Click on your Backend service** (the service name)
3. **Click the "Settings" tab** (gear icon or "Settings" link)
4. **Scroll down to find "Root Directory"** section
5. **In the "Root Directory" field, type:** `backend`
6. **Click "Save" or "Update"**
7. **Railway will automatically redeploy**

#### For Frontend Service:

1. **Click on your Frontend service** (the service name)
2. **Click the "Settings" tab**
3. **Find "Root Directory" section**
4. **In the "Root Directory" field, type:** `frontend`
5. **Click "Save" or "Update"**
6. **Railway will automatically redeploy**

## Visual Guide

After clicking on your service, you should see settings like:

```
Settings
├── Service Name
├── Root Directory  ← SET THIS TO: backend (or frontend)
├── Build Command
├── Start Command
└── ...
```

## Verification

After setting Root Directory:

1. **Check the build logs** - you should see:
   - ✅ "Found Dockerfile at backend/Dockerfile" (or frontend/Dockerfile)
   - ✅ "Building with Dockerfile"
   - ❌ NOT "Railpack" or "Nixpacks"

2. **The error should disappear** and build should start

## If You Don't See "Root Directory" Option

If you can't find the Root Directory setting:

1. **Delete the current service** (or create a new one)
2. **When creating a new service:**
   - Click "New" → "GitHub Repo"
   - Select your repository
   - **BEFORE clicking "Deploy"**, look for "Settings" or "Configure"
   - Set Root Directory there
   - Then deploy

## Alternative: Use Railway CLI

If dashboard doesn't work, use Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Set root directory for backend
cd backend
railway service
# Select backend service, then set root directory

# Set root directory for frontend  
cd ../frontend
railway service
# Select frontend service, then set root directory
```

## Why This Happens

Railway defaults to looking for files in the repository root. Since your Dockerfiles are in subdirectories (`backend/` and `frontend/`), you must tell Railway where to look by setting the Root Directory.

## Quick Checklist

- [ ] Backend service: Root Directory = `backend` ✅
- [ ] Frontend service: Root Directory = `frontend` ✅
- [ ] Both services saved and redeployed ✅
- [ ] Build logs show "Building with Dockerfile" ✅
- [ ] No more "Railpack" errors ✅

## Still Having Issues?

If Root Directory is set but still not working:

1. **Double-check spelling**: Must be exactly `backend` or `frontend` (lowercase, no trailing slash)
2. **Verify Dockerfile exists**: Check that `backend/Dockerfile` and `frontend/Dockerfile` exist in your repo
3. **Check file is committed**: Make sure Dockerfiles are committed to Git
4. **Try redeploying**: Manually trigger a new deployment after setting root directory

