# MedSim Ads Integration Guide

## Overview
This document outlines the integration of Google AdSense for monetizing the MedSim medical education platform across all browsers (desktop and mobile).

## Technology Choice: Google AdSense

### Why AdSense Only
- **Universal Browser Support**: Works seamlessly on desktop, mobile web, and PWA
- **Single Integration**: One codebase for all platforms
- **Responsive Ads**: Automatically adapts to screen sizes
- **No App Store Requirements**: No need for separate mobile SDK
- **Simplified Management**: Single dashboard for all ad revenue

### Benefits for MedSim
- **Medical Content Safe**: Google's strict health content policies align with educational goals
- **Performance**: Async loading with minimal impact on page speed
- **Revenue Optimization**: Auto-sizing units maximize revenue across devices
- **Global Fill**: High fill rates worldwide for educational content

## Implementation Strategy

### 1. Progressive Enhancement
- Ads load after core medical simulation content
- Uses requestIdleCallback for non-blocking insertion
- Graceful degradation when ads cannot load

### 2. User Experience First
- Single banner placement below main content
- No ads during active patient interactions or diagnoses
- Clean loading states without disrupting medical scenarios

### 3. Mobile Optimization
- Responsive banner units work perfectly on mobile browsers
- No need for app-specific implementations
- PWA users get same experience as web users

## Configuration

### Environment Variables
```bash
# Google AdSense
ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX
ADSENSE_SLOT_ID=YYYYYYYYYY  # Optional: Auto ads recommended
```

### Testing Configuration
For development, use Google's test values:
```bash
ADSENSE_CLIENT_ID=ca-pub-0000000000000000
ADSENSE_SLOT_ID=test
```

## Ad Placement Guidelines

### Desktop Layout (≥1200px)
- **Position**: Fixed on right side, vertically centered
- **Size**: 160x600 (Wide Skyscraper)
- **Behavior**: Always visible, does not interfere with content

### Tablet/Small Desktop (769px-1199px)
- **Position**: Fixed at bottom center
- **Size**: 320x50 (Banner)
- **Behavior**: Small, unobtrusive banner

### Mobile Layout (<768px)
- **Position**: Fixed at bottom of viewport
- **Size**: 320x50 (Mobile Banner)
- **Behavior**: Minimal height to preserve screen space

### PWA Considerations
- Same implementation as mobile web
- No additional configuration needed
- Cached for offline functionality (ads won't show offline)

## Revenue Optimization

### Best Practices
1. **Auto Ads**: Let Google optimize placements
2. **Viewability**: Ensure ads are in viewport
3. **Page Speed**: Lazy load after content
4. **Content Quality**: High-quality medical content = better CPMs

### Expected Performance
- **Fill Rate**: 95%+ in major markets
- **eCPM**: $2-5 for medical/education niche
- **Mobile Performance**: Similar to desktop with responsive units

## Integration Details

### HTML Implementation
```html
<!-- In <head> -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" 
        data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"></script>

<!-- Ad placement -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

### Performance Optimization
```javascript
// Lazy load ads after page content
if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
        // Initialize ads
    });
} else {
    setTimeout(() => {
        // Initialize ads
    }, 1);
}
```

## Compliance & Safety

### Medical Content Guidelines
- No ads on pages with graphic medical imagery
- Avoid placement near emergency medical information
- Comply with Google's health content policies

### Privacy Requirements
- Update Privacy Policy for ad data collection
- Implement consent management for GDPR/CCPA
- Provide ad preference controls

### Content Security Policy
Add to CSP headers:
```
script-src 'self' *.googlesyndication.com *.googleadservices.com;
img-src 'self' *.googlesyndication.com *.doubleclick.net;
frame-src *.googlesyndication.com;
```

## Monitoring & Analytics

### Key Metrics
- Page RPM (Revenue per thousand pages)
- Ad viewability rate
- User engagement impact
- Mobile vs desktop performance

### Logging Integration
- Track ad impressions in session logs
- Monitor load time impact
- Correlate with user retention

## Testing Checklist

- [ ] Ads display correctly on desktop browsers
- [ ] Ads display correctly on mobile browsers
- [ ] PWA shows ads when online
- [ ] No ads interfere with medical simulations
- [ ] Page load time remains under 3 seconds
- [ ] Ad blockers handled gracefully
- [ ] CSP headers configured correctly

## Support & Resources

- [Google AdSense Documentation](https://support.google.com/adsense)
- [AdSense Policy Center](https://support.google.com/adsense/topic/1261918)
- [Responsive Ad Units Guide](https://support.google.com/adsense/answer/9183460)
- [Health Content Policies](https://support.google.com/adsense/answer/9335567)