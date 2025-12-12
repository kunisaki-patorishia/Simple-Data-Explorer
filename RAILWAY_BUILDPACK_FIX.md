# Fix: Railway Buildpack Error

## The Problem
Railway is trying to use a buildpack instead of Docker, causing the error:
```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

## Solution: Force Docker Build

Railway needs to be explicitly told to use Docker instead of buildpacks.

### Option 1: Set Build Type in Railway Dashboard (Easiest)

1. **Go to your service in Railway dashboard**
2. **Click on the service** (Backend or Frontend)
3. **Go to Settings tab**
4. **Find "Build Type" or "Builder" setting**
5. **Change it to: `Dockerfile`** (not "Nixpacks" or "Buildpack")
6. **Make sure "Root Directory" is set correctly:**
   - Backend: `backend`
   - Frontend: `frontend`
7. **Save and redeploy**

### Option 2: Use railway.toml (More Reliable)

I've created `railway.toml` files in both `backend/` and `frontend/` directories. These explicitly tell Railway to use Docker.

**After pushing the changes:**
1. Railway will automatically detect the `railway.toml` files
2. It will use Docker instead of buildpacks
3. Redeploy your services

### Option 3: Manual Configuration

If the above doesn't work:

1. **Delete the service** (or create a new one)
2. **When creating the service:**
   - Select "Deploy from GitHub repo"
   - **IMPORTANT**: Before deploying, go to Settings
   - Set **Root Directory**: `backend` or `frontend`
   - Set **Build Type**: `Dockerfile`
   - Railway will now use the Dockerfile

## Verification

After applying the fix:
- Check build logs - should show "Building with Dockerfile"
- Should NOT see "Nixpacks" or "Buildpack" in logs
- Build should complete successfully

## Common Issues

**Still seeing buildpack error?**
- Make sure Root Directory is set correctly
- Make sure railway.toml files are in the correct directories
- Try deleting and recreating the service
- Check that Dockerfile exists in the root directory (backend/ or frontend/)

**Dockerfile not found?**
- Verify Root Directory is set to `backend` or `frontend`
- Check that Dockerfile exists in that directory
- Make sure Dockerfile is committed to Git

## Quick Checklist

- [ ] Root Directory set to `backend` (for backend service)
- [ ] Root Directory set to `frontend` (for frontend service)
- [ ] Build Type set to `Dockerfile` (not Nixpacks)
- [ ] railway.toml files exist in backend/ and frontend/
- [ ] Dockerfile exists in backend/ and frontend/
- [ ] Changes committed and pushed to GitHub
- [ ] Service redeployed after changes

