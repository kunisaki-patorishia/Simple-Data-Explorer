# Fixing Railway Dockerfile Error

## The Problem
Railway couldn't find the Dockerfile because it was looking in the root directory, but your Dockerfiles are in `backend/` and `frontend/` folders.

## Solution: Set Root Directory in Railway

### For Backend Service:

1. **Go to your Railway project dashboard**
2. **Click on your Backend service**
3. **Go to Settings tab**
4. **Find "Root Directory" setting**
5. **Set it to**: `backend`
6. **Save changes**

Railway will now look for `Dockerfile` in the `backend/` directory.

### For Frontend Service:

1. **Go to your Railway project dashboard**
2. **Click on your Frontend service**
3. **Go to Settings tab**
4. **Find "Root Directory" setting**
5. **Set it to**: `frontend`
6. **Save changes**

Railway will now look for `Dockerfile` in the `frontend/` directory.

## Alternative: Deploy from Subdirectories

When creating a new service in Railway:

1. **Click "New" → "GitHub Repo"**
2. **Select your repository**
3. **In the deployment settings, set "Root Directory" to:**
   - `backend` for backend service
   - `frontend` for frontend service
4. Railway will automatically find the Dockerfile in that directory

## Verify

After setting the root directory:
- Railway should detect the Dockerfile automatically
- The build should start successfully
- Check the build logs to confirm

## Quick Checklist

- [ ] Backend service has Root Directory = `backend`
- [ ] Frontend service has Root Directory = `frontend`
- [ ] Both services are redeployed after changing root directory
- [ ] Build logs show Dockerfile found successfully

