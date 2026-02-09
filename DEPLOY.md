# 🚀 Deployment Guide - Data Converter API

**Choose your platform and follow the steps below.**

---

## Option 1: Deploy to Render.com (RECOMMENDED - FREE)

Render.com gives you **750 hours/month of free hosting** = **24/7 uptime**

### Step 1: Create GitHub Repository

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Data Converter API"

# Create main branch
git branch -M main

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/data-converter-api.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to:** https://render.com
2. **Sign up** (free account with GitHub)
3. **Click:** "New Web Service"
4. **Connect GitHub:**
   - Select your `data-converter-api` repository
   - Click "Connect"

5. **Configure Service:**
   - **Name:** `data-converter-api`
   - **Runtime:** Python 3.11
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** 
     ```
     gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120
     ```
   - **Plan:** Free

6. **Add Environment Variables:**
   - Click "Advanced"
   - Add variable:
     - **Key:** `DATABASE_URL`
     - **Value:** `sqlite:///./converter.db`
   - Add variable:
     - **Key:** `API_KEY_REQUIRED`
     - **Value:** `false`
   - Add variable:
     - **Key:** `PYTHONUNBUFFERED`
     - **Value:** `1`

7. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for build

**Done!** Your API is live at:
```
https://data-converter-api.onrender.com
```

### Test Your Deployment

```bash
# Health check
curl https://data-converter-api.onrender.com/health

# API info
curl https://data-converter-api.onrender.com/

# Test conversion
curl -X POST https://data-converter-api.onrender.com/api/v1/csv-to-json \
  -F "file=@test_data.csv"
```

---

## Option 2: Deploy to Railway.app (FREE with $5 credit)

### Step 1: Create GitHub Repo (same as above)

### Step 2: Deploy on Railway

1. **Go to:** https://railway.app
2. **Sign up** (free with GitHub)
3. **Click:** "New Project"
4. **Select:** "Deploy from GitHub repo"
5. **Connect** your GitHub account
6. **Select** your `data-converter-api` repository
7. **Fill Variables:**
   - `DATABASE_URL` = `sqlite:///./converter.db`
   - `API_KEY_REQUIRED` = `false`

8. **Deploy** (automatic)

Your app runs with $5 free credit/month

---

## Option 3: Deploy to PythonAnywhere (FREE)

### Step 1: Create Account
- Go to https://pythonanywhere.com
- Sign up (free account)

### Step 2: Upload Code
- Go to "Files" tab
- Upload main.py, requirements.txt
- Run in Bash console:
  ```bash
  pip install -r requirements.txt
  ```

### Step 3: Create Web App
- Click "Web" → "Add a new web app"
- Choose Python 3.11
- Choose "Manual configuration"
- Fill in the application path and WSGI file

### Step 4: Configure WSGI
Edit WSGI file to:
```python
import sys
sys.path.insert(0, '/home/yourusername/mysite')
from main import app
application = app
```

Your app runs at: `yourusername.pythonanywhere.com`

---

## Option 4: Docker Deployment (Advanced)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD ["gunicorn", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

Deploy:
```bash
# Build
docker build -t data-converter-api .

# Run
docker run -p 8000:8000 data-converter-api
```

---

## Option 5: Local/VPS Deployment

### Requirements
- Python 3.8+
- Linux/Mac/Windows

### Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4
   ```

3. **Use Systemd** (Linux only):
   
   Create `/etc/systemd/system/converter-api.service`:
   ```
   [Unit]
   Description=Data Converter API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/project
   ExecStart=/usr/bin/gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Run:
   ```bash
   sudo systemctl start converter-api
   sudo systemctl enable converter-api
   ```

4. **Use Nginx as reverse proxy:**

   Edit `/etc/nginx/sites-available/default`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
       }
   }
   ```

   Reload Nginx:
   ```bash
   sudo nginx -s reload
   ```

---

## Option 6: AWS Deployment (Paid - starts free)

### Using AWS Elastic Beanstalk

1. **Install AWS CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p python-3.11 data-converter-api
   ```

3. **Deploy:**
   ```bash
   eb create production
   eb deploy
   ```

Your app runs at: `production.elasticbeanstalk.com`

---

## ✅ After Deployment

### Step 1: Test Your API
```bash
curl https://your-api-url/health
curl https://your-api-url/docs
```

### Step 2: Add Custom Domain (Optional)
Most platforms support custom domains. Add your domain:
- Render: Settings → Custom Domain
- Railway: Settings → Custom Domain
- AWS: Route 53

### Step 3: Monitor & Logs
- Render: Dashboard → Logs
- Railway: View logs in dashboard
- AWS: CloudWatch

---

## 🎯 Recommended: Render.com

**Why Render.com?**
- ✅ Free hosting (750 hours/month)
- ✅ Auto-deploys on git push
- ✅ Free SSL certificate
- ✅ Easy to scale
- ✅ Great for beginners

**Cost:** $0/month (free tier) → $7+/month (paid tier)

---

## 🚀 Quick Summary

| Platform | Cost | Setup Time | Best For |
|----------|------|-----------|----------|
| **Render** | Free | 5 min | Beginners |
| **Railway** | Free ($5/mo) | 5 min | Beginners |
| **PythonAnywhere** | Free | 10 min | Learning |
| **Docker** | Your cost | 15 min | Advanced |
| **VPS** | $5-50/mo | 30 min | Full control |
| **AWS** | Free tier → paid | 20 min | Scaling |

---

## 📊 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Requirements.txt verified
- [ ] .env variables configured
- [ ] Deployment platform selected
- [ ] App deployed successfully
- [ ] Health check passing
- [ ] Can access /docs
- [ ] Test conversion works
- [ ] Database created
- [ ] Logs checked
- [ ] API is live!

---

## 🐛 Troubleshooting

### "Build failed"
- Check `requirements.txt` is correct
- Verify Python version compatibility
- Check for syntax errors in main.py

### "502 Bad Gateway"
- Check logs for error messages
- Restart application
- Verify environment variables

### "Connection refused"
- Database might not exist
- Check DATABASE_URL is correct
- Recreate database if needed

### "Timeout error"
- Increase timeout value in start command
- Optimize slow endpoints
- Check file sizes

---

## 🎉 You're Deployed!

Once your API is live:

1. **Test it:** `https://your-api-url/docs`
2. **Share it:** ProductHunt, Dev.to, Twitter
3. **Get users:** Watch signups flow in
4. **Make money:** 10% convert to Pro = revenue! 💰

---

**Happy deploying! 🚀**
