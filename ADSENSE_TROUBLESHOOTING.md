# AdSense Troubleshooting Guide

## Common Issues and Solutions

### 1. Ads Not Showing - Checklist

#### Environment Variables
- **Issue**: Missing or incorrectly formatted AdSense client ID
- **Solution**: Ensure `ADSENSE_CLIENT_ID` includes the `ca-` prefix
  ```bash
  # Correct format
  ADSENSE_CLIENT_ID=ca-pub-2269485035404816
  
  # Wrong format (missing ca- prefix)
  ADSENSE_CLIENT_ID=pub-2269485035404816
  ```

#### API Response Check
1. Open browser developer console (F12)
2. Go to Network tab
3. Look for `/api/config/adsense` request
4. Verify response contains:
   ```json
   {
     "enabled": true,
     "client_id": "ca-pub-2269485035404816",
     "slot_id": "auto"
   }
   ```

#### Console Debugging
Check browser console for these messages:
- `AdSense config loaded:` - Should show your configuration
- `AdSense script loaded successfully` - Script loaded from Google
- `Creating ad, container found: true` - Container element exists
- `Ad unit created: 320x50 at mobile-bottom` - Ad unit dimensions

### 2. Test Your Configuration

Visit `/static/test-adsense.html` to run a comprehensive test that checks:
- API configuration
- Script loading
- Ad container creation
- Console output

### 3. Common Error Messages

#### "AdSense not enabled or missing config"
- **Cause**: Environment variables not set
- **Fix**: Set `ADSENSE_CLIENT_ID` in your environment

#### "Failed to load AdSense script"
- **Cause**: Network issues or ad blocker
- **Fix**: 
  - Disable ad blockers
  - Check network connectivity
  - Verify CSP headers allow Google domains

#### Container not found
- **Cause**: DOM element missing
- **Fix**: Ensure `adsense-container` div exists in HTML

### 4. Platform-Specific Issues

#### Local Development
```bash
# Set environment variables before running
export ADSENSE_CLIENT_ID=ca-pub-2269485035404816
export ADSENSE_SLOT_ID=auto
python run_server.py
```

#### AWS Elastic Beanstalk
1. Go to EB Console → Configuration → Software
2. Add environment properties:
   - `ADSENSE_CLIENT_ID`: `ca-pub-2269485035404816`
   - `ADSENSE_SLOT_ID`: `auto`
3. Apply configuration and restart

#### Docker
Add to docker-compose.yml:
```yaml
environment:
  - ADSENSE_CLIENT_ID=ca-pub-2269485035404816
  - ADSENSE_SLOT_ID=auto
```

### 5. Verification Steps

1. **Check Environment Variables**
   ```python
   # In Python console
   import os
   print(os.getenv('ADSENSE_CLIENT_ID'))  # Should show ca-pub-...
   ```

2. **Test API Endpoint**
   ```bash
   curl http://localhost:8000/api/config/adsense
   ```

3. **Browser Developer Tools**
   - Network tab: Check for blocked requests
   - Console tab: Look for error messages
   - Elements tab: Verify `.adsbygoogle` element exists

### 6. Ad Display Timeline

Ads may not appear immediately because:
1. **First Load**: AdSense needs to approve your domain (can take hours)
2. **Low Traffic**: Test ads may not always show
3. **Geographic Restrictions**: Some regions have limited ad inventory

### 7. Mobile vs Desktop

- **Desktop (≥1200px)**: Look for 160x600 ad on right side
- **Tablet (769-1199px)**: Look for 320x50 ad at bottom center
- **Mobile (<768px)**: Look for 320x50 ad at bottom

### 8. Quick Debug Script

Add this to browser console to test:
```javascript
// Check if AdSense is configured
fetch('/api/config/adsense')
  .then(r => r.json())
  .then(config => {
    console.log('AdSense Config:', config);
    console.log('Container exists:', !!document.getElementById('adsense-container'));
    console.log('AdSense script loaded:', !!window.adsbygoogle);
  });
```

## Still Not Working?

1. Clear browser cache and cookies
2. Try incognito/private browsing mode
3. Test with a different browser
4. Check if ads.txt file is needed for your domain
5. Verify your AdSense account is approved and active