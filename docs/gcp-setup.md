# GCP Cloud Run Setup Guide

Complete step-by-step guide to deploy ScribeFlow to Google Cloud Run with GitHub Actions CI/CD.

---

## 📋 Prerequisites

- Google Cloud account with free tier activated
- GitHub repository for ScribeFlow
- `gcloud` CLI installed (optional, for local testing)

---

## 🚀 Setup Steps

### Step 1: Create GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Enter project details:
   - **Project name**: `scribeflow-portfolio` (or your choice)
   - **Project ID**: Note this down (e.g., `scribeflow-portfolio-123456`)
4. Click **Create**

> [!TIP]
> The Project ID must be globally unique. GCP will suggest one if your choice is taken.

---

### Step 2: Enable Required APIs

1. In GCP Console, go to **APIs & Services** → **Library**
2. Search and enable these APIs:
   - **Cloud Run API**
   - **Container Registry API** (or **Artifact Registry API**)
   - **Cloud Build API**

Or use `gcloud` CLI:
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

### Step 3: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Enter details:
   - **Name**: `github-actions-deployer`
   - **Description**: `Service account for GitHub Actions CI/CD`
4. Click **Create and Continue**

5. **Grant roles** (click "Add Another Role" for each):
   - `Cloud Run Admin`
   - `Service Account User`
   - `Storage Admin` (for Container Registry)

6. Click **Done**

---

### Step 4: Create Service Account Key

1. Find your service account in the list
2. Click the **three dots** (⋮) → **Manage keys**
3. Click **Add Key** → **Create new key**
4. Choose **JSON** format
5. Click **Create**
6. **Save the JSON file securely** (you'll need this for GitHub)

> [!CAUTION]
> This JSON file contains sensitive credentials. Never commit it to Git or share it publicly.

---

### Step 5: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these two secrets:

#### Secret 1: `GCP_PROJECT_ID`
- **Name**: `GCP_PROJECT_ID`
- **Value**: Your GCP Project ID (e.g., `scribeflow-portfolio-123456`)

#### Secret 2: `GCP_SA_KEY`
- **Name**: `GCP_SA_KEY`
- **Value**: Paste the **entire contents** of the JSON key file you downloaded

> [!IMPORTANT]
> Copy the entire JSON file contents, including the curly braces `{ }`.

---

### Step 6: Delete Compute Engine VM (If Created)

If you created a VM instance earlier:

1. Go to **Compute Engine** → **VM instances**
2. Select your VM
3. Click **Delete**
4. Confirm deletion

This ensures you're only using Cloud Run (free tier).

---

### Step 7: First Deployment

#### Option A: Push to Main Branch (Automatic)
```bash
# Make any change to your code
git add .
git commit -m "Initial Cloud Run deployment"
git push origin main
```

The GitHub Action will automatically:
1. Build Docker image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Provide a public URL

#### Option B: Manual Deployment
1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Manual Deploy to Cloud Run**
4. Click **Run workflow**
5. Choose options and click **Run workflow**

---

### Step 8: Monitor Deployment

1. In GitHub, go to **Actions** tab
2. Click on the running workflow
3. Watch the deployment progress
4. Once complete, you'll see the service URL in the logs

Or check in GCP Console:
1. Go to **Cloud Run**
2. Click on `scribeflow` service
3. Copy the **URL** at the top

---

### Step 9: Test Your Deployment

Visit your Cloud Run URL:
```
https://scribeflow-XXXXXXXXXX-uc.a.run.app/docs
```

You should see the FastAPI interactive documentation!

Test the API:
```bash
curl https://YOUR-CLOUD-RUN-URL.run.app/docs
```

---

## 🎯 Free Tier Limits

Your deployment stays **FREE** within these limits:

| Resource | Free Tier Limit | Typical Portfolio Usage |
|----------|----------------|------------------------|
| Requests | 2 million/month | ✅ ~1000/month |
| Compute time | 360,000 GB-seconds | ✅ ~5000 GB-seconds |
| Network egress | 1 GB/month | ✅ ~100 MB |

**Result**: $0/month for normal portfolio traffic! 🎉

---

## 🔧 Configuration Options

### Adjust Resources (in `.github/workflows/deploy.yml`)

```yaml
--memory 2Gi          # RAM allocation (512Mi, 1Gi, 2Gi, 4Gi)
--cpu 2               # CPU allocation (1, 2, 4)
--timeout 300         # Request timeout (seconds)
--max-instances 10    # Max concurrent instances
```

### Environment Variables

Add environment variables in the workflow:
```yaml
--set-env-vars "KEY1=value1,KEY2=value2"
```

---

## 🐛 Troubleshooting

### Deployment fails with "Permission denied"
- Verify service account has correct roles
- Check `GCP_SA_KEY` secret is valid JSON

### "API not enabled" error
- Enable required APIs in Step 2
- Wait 1-2 minutes for APIs to activate

### Docker build fails
- Check `Dockerfile` syntax
- Verify all dependencies in `requirements.txt`

### Service URL returns 404
- Check Cloud Run logs in GCP Console
- Verify app runs on port 5000 (or update Dockerfile)

---

## 📊 Monitoring & Logs

### View Logs
1. Go to **Cloud Run** in GCP Console
2. Click on `scribeflow` service
3. Click **Logs** tab

Or use `gcloud`:
```bash
gcloud run services logs read scribeflow --region us-central1
```

### View Metrics
1. In Cloud Run service page
2. Click **Metrics** tab
3. See request count, latency, errors

---

## 🔄 Rollback to Previous Version

If a deployment has issues:

### Option 1: Via GCP Console
1. Go to **Cloud Run** → `scribeflow`
2. Click **Revisions** tab
3. Select previous working revision
4. Click **Manage Traffic**
5. Set 100% traffic to old revision

### Option 2: Via GitHub Actions
1. Go to **Actions** → **Manual Deploy**
2. Run workflow with previous commit SHA as tag

---

## 🎓 Portfolio Tips

### Add Deployment Badge to README

```markdown
![Deploy Status](https://github.com/YOUR-USERNAME/ScribeFlow/actions/workflows/deploy.yml/badge.svg)
```

### Showcase in Portfolio
- ✅ Live demo URL
- ✅ "Deployed with CI/CD pipeline"
- ✅ "Serverless architecture on GCP Cloud Run"
- ✅ "Automated Docker builds with GitHub Actions"

---

## 📚 Next Steps

- [ ] Set up custom domain (optional)
- [ ] Add Cloud Monitoring alerts
- [ ] Implement staging environment
- [ ] Add automated tests in CI/CD
- [ ] Configure Cloud CDN for faster response

---

## 🆘 Getting Help

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [ScribeFlow Issues](https://github.com/dreww01/ScribeFlow/issues)

---

**🎉 Congratulations!** Your ScribeFlow project is now deployed with professional CI/CD! Every push to `main` automatically deploys to production.
