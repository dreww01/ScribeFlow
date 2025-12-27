# Quick Reference: GCP Cloud Run Deployment

## 🚀 One-Time Setup Checklist

Follow these steps once to set up automated deployment:

### 1. Create GCP Project
- [ ] Go to [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Create new project (e.g., `scribeflow-portfolio`)
- [ ] Note your **Project ID**

### 2. Enable APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

Or enable manually in GCP Console → APIs & Services → Library

### 3. Create Service Account
- [ ] Go to **IAM & Admin** → **Service Accounts**
- [ ] Create service account: `github-actions-deployer`
- [ ] Add roles:
  - `Cloud Run Admin`
  - `Service Account User`
  - `Storage Admin`
- [ ] Create JSON key and download it

### 4. Configure GitHub Secrets
- [ ] Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
- [ ] Add secret `GCP_PROJECT_ID` = your project ID
- [ ] Add secret `GCP_SA_KEY` = entire JSON key contents

### 5. Deploy!
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

Watch deployment in **Actions** tab!

---

## 📝 Common Commands

### View Logs
```bash
gcloud run services logs read scribeflow --region us-central1
```

### Get Service URL
```bash
gcloud run services describe scribeflow --region us-central1 --format 'value(status.url)'
```

### Manual Deploy
```bash
gcloud run deploy scribeflow \
  --image gcr.io/PROJECT_ID/scribeflow:latest \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Check service account roles |
| API not enabled | Enable required APIs, wait 2 minutes |
| Build fails | Check Dockerfile and requirements.txt |
| 404 on URL | Check Cloud Run logs for errors |

---

## 💰 Free Tier Limits

- 2 million requests/month
- 360,000 GB-seconds compute
- 1 GB network egress

**Your portfolio traffic = FREE!** 🎉

---

For detailed instructions, see [docs/gcp-setup.md](../docs/gcp-setup.md)
