# Deployment Guide - Hokito Game to Render (FREE)

This guide will help you deploy your Hokito multiplayer game to the internet for **FREE** using Render.

## Prerequisites

- A GitHub account (free)
- A Render account (free) - sign up at https://render.com

## Step 1: Configure Git

First, set up your Git identity (only need to do this once):

```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

Then commit your code:

```bash
cd hokito-game
git add .
git commit -m "Initial commit - Hokito multiplayer game"
```

## Step 2: Push to GitHub

1. Go to https://github.com and create a new repository called `hokito-game`
2. **Don't initialize** with README, .gitignore, or license (we already have these)
3. Copy the repository URL (it will look like: `https://github.com/YOUR-USERNAME/hokito-game.git`)
4. Run these commands:

```bash
git remote add origin https://github.com/YOUR-USERNAME/hokito-game.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Render

### Create a Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### Deploy Your App

1. **From Render Dashboard:**
   - Click "New +" button
   - Select "Web Service"

2. **Connect GitHub:**
   - Click "Connect GitHub"
   - Find and select your `hokito-game` repository
   - Click "Connect"

3. **Configure the Service:**
   Fill in these settings:

   - **Name**: `hokito-game` (or any name you want)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Instance Type**: `Free`

4. **Advanced Settings** (click to expand):
   - **Auto-Deploy**: Enable (recommended)
   - Leave everything else as default

5. **Click "Create Web Service"**

## Step 4: Wait for Deployment

Render will now:
1. Clone your repository
2. Install dependencies
3. Build your frontend
4. Start your server

This takes about 5-10 minutes for the first deployment.

## Step 5: Get Your URL

Once deployment is complete:
- Your app will be live at: `https://hokito-game-xxxx.onrender.com`
- The URL will be shown in the Render dashboard
- Copy this URL and share it with friends!

## How to Play Online

1. **Player 1**: Go to your Render URL
2. **Player 2**: Go to the same URL
3. Player 1 creates a game and shares the room code
4. Player 2 joins with the code
5. Play!

## Important Notes

### Free Tier Limitations
- Server "sleeps" after 15 minutes of inactivity
- Wakes up when someone visits (takes ~30 seconds)
- Perfect for playing with friends occasionally
- No cost at all!

### To Upgrade (Optional)
- If you want 24/7 instant access
- Go to your service → Settings → Instance Type
- Change to "Starter" ($7/month)
- This keeps your server always awake

## Updating Your Game

Whenever you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Render will automatically rebuild and redeploy! (if Auto-Deploy is enabled)

## Troubleshooting

### Build Failed
- Check the Render logs in the dashboard
- Make sure all dependencies are in package.json
- Contact support if needed

### Can't Connect to Game
- Make sure your Render service is "Live" (not "Deploying")
- Check browser console for errors (F12)
- Try refreshing the page

### Players Can't Find Each Other
- Both players must use the SAME URL (your Render URL)
- Make sure the room code is entered correctly
- Try creating a new game

## Custom Domain (Optional)

Want `hokito.yourname.com` instead of the Render URL?

1. Buy a domain (from Namecheap, Google Domains, etc.)
2. In Render dashboard: Settings → Custom Domain
3. Add your domain
4. Update DNS records as instructed by Render
5. Done!

## Cost Summary

**FREE TIER:**
- Cost: $0/month
- Sleep after inactivity: Yes
- Good for: Casual play with friends

**PAID TIER ($7/mo):**
- Cost: $7/month
- Always online: Yes
- Good for: Frequent play, public access

## Support

If you need help:
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- GitHub Issues: Create an issue in your repo

---

**Congratulations!** Your game is now on the internet! 🎉

Share your URL with friends and enjoy playing Hokito online!
