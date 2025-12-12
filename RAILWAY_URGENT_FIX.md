# ⚠️ URGENT: Root Directory Not Set in Railway Dashboard

## The Problem

Your error shows:
```
root_dir=  ← THIS IS EMPTY!
```

**Railway cannot find your Dockerfile because Root Directory is not set in the dashboard.**

## ✅ SOLUTION: Set Root Directory in Railway Dashboard

### Step 1: Access Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Log in to your account
3. Click on your project

### Step 2: Fix Backend Service

1. **Click on your Backend service** (it might be named something like "web" or "backend" or the repo name)
2. Look for tabs at the top: **Deployments | Metrics | Logs | Settings | Variables**
3. **Click on "Settings" tab**
4. Scroll down to find **"Root Directory"** section
5. You'll see a text input field (might be empty or show `/`)
6. **Type exactly:** `backend` (lowercase, no quotes, no slash)
7. **Click "Save" or "Update"** button
8. Railway will automatically trigger a new deployment

### Step 3: Fix Frontend Service

1. **Click on your Frontend service** (in the same project)
2. **Click on "Settings" tab**
3. Find **"Root Directory"** section
4. **Type exactly:** `frontend` (lowercase, no quotes, no slash)
5. **Click "Save" or "Update"** button
6. Railway will automatically trigger a new deployment

## Where to Find Root Directory Setting

The Settings page should look like this:

```
┌─────────────────────────────────────┐
│ Service Settings                    │
├─────────────────────────────────────┤
│ Service Name: [your-service-name]   │
│                                     │
│ Root Directory: [backend    ] ← SET THIS!
│                                     │
│ Build Command: (auto-detected)      │
│ Start Command: (auto-detected)      │
│                                     │
│ [Save] [Cancel]                     │
└─────────────────────────────────────┘
```

## If You Don't See "Root Directory" Option

**Option A: Your Railway UI might be different**

1. Look for "Configuration" or "Build Settings"
2. Or look for "Deploy" settings
3. Root Directory might be in a different section

**Option B: Delete and Recreate Service**

1. **Delete the current service** (Settings → Delete Service)
2. **Create a new service:**
   - Click "New" → "GitHub Repo"
   - Select your repository
   - **BEFORE clicking "Deploy"**, look for a "Configure" or "Settings" button
   - Set Root Directory there
   - Then click "Deploy"

**Option C: Use Railway CLI**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# For Backend
cd backend
railway service
# Select your backend service
# Then run:
railway variables set RAILWAY_ROOT_DIRECTORY=backend

# For Frontend  
cd ../frontend
railway service
# Select your frontend service
# Then run:
railway variables set RAILWAY_ROOT_DIRECTORY=frontend
```

## Verification

After setting Root Directory, check the build logs. You should see:

✅ **GOOD:**
```
Found Dockerfile at backend/Dockerfile
Building with Dockerfile
```

❌ **BAD (what you're seeing now):**
```
root_dir=
skipping 'Dockerfile' at 'backend/Dockerfile'
using build driver railpack
```

## Still Not Working?

1. **Double-check the spelling**: Must be exactly `backend` or `frontend` (no capital letters, no trailing slash)
2. **Make sure you saved**: Click the Save button after entering the value
3. **Check if deployment triggered**: After saving, a new deployment should start automatically
4. **Try deleting and recreating**: Sometimes Railway needs a fresh start

## Quick Test

After setting Root Directory:
1. Wait for the new deployment to start
2. Check the build logs
3. You should see "Building with Dockerfile" instead of "Railpack"

## Need Help?

If you still can't find the Root Directory setting:
1. Take a screenshot of your Railway Settings page
2. Check Railway's documentation: https://docs.railway.app
3. The setting might be in a different location in newer Railway UI versions

**The key is: Root Directory MUST be set in the Railway dashboard - it cannot be set via config files alone!**

