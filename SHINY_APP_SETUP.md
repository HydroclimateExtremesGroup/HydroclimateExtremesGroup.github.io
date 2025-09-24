# Wisconsin Rainfall Project - Shiny App Integration Guide

## Overview
This guide documents the integration of the existing Wisconsin Rainfall Project Shiny app (hosted on ShinyApps.io) into your GitHub Pages website.

## Current Setup
The Wisconsin Rainfall Project app is already deployed and accessible at:
**https://wisconsinrainfallproject.shinyapps.io/rainyday_web_application/**

## Integration Status
✅ **COMPLETED** - The app is now integrated into your website at `/wisconsin-rainfall-project.html`

## App Features
The Wisconsin Rainfall Project app provides interactive access to:

- **Duration Selection**: 3 hours, 6 hours, 12 hours, 24 hours, 48 hours, 4 days, 10 days
- **Recurrence Intervals**: 2-year, 5-year, 10-year, 25-year, 50-year, 100-year, 200-year, 500-year, 1000-year
- **Unit Types**: mm (depth), in (depth), mm/hr (intensity), in/hr (intensity)
- **Data Sources**:
  - Present Conditions (RainyDay, NOAA Atlas 14, Comparison)
  - Climate Projections (low/high emissions scenarios for 2001-2030, 2041-2070, 2071-2100)

### Available Tabs:
1. **Precipitation Frequency Tabular** - Data tables with download options
2. **Precipitation Frequency Graphical** - Interactive charts with confidence intervals
3. **Future Climate Results** - Climate projection data and visualizations
4. **RainyDay-Atlas14 Comparison** - Comparative analysis between data sources

## Step 1: Prepare Your Shiny App

1. **Organize your Shiny app files** in a directory structure like this:
   ```
   wisconsin-rainfall-app/
   ├── app.R (or ui.R + server.R)
   ├── data/
   │   ├── rainfall_data.csv
   │   └── other_data_files...
   ├── www/
   │   ├── styles.css (optional)
   │   └── images/ (optional)
   └── README.md (optional)
   ```

2. **Ensure your app is self-contained** - all data files and dependencies should be included.

## Step 2: Install and Use Shinylive

1. **Install the shinylive package**:
   ```r
   install.packages("shinylive")
   ```

2. **Export your Shiny app**:
   ```r
   library(shinylive)
   
   # Export your app to the docs directory
   shinylive::export(
     appdir = "wisconsin-rainfall-app",  # Path to your Shiny app
     destdir = "docs"                   # Output directory for GitHub Pages
   )
   ```

3. **Test locally** (optional but recommended):
   ```r
   install.packages("httpuv")
   library(httpuv)
   httpuv::runStaticServer("docs/", port = 8008)
   ```
   Then visit `http://localhost:8008` to test your app.

## Step 3: Configure GitHub Pages

1. **Commit and push your changes**:
   ```bash
   git add docs/
   git commit -m "Add Wisconsin Rainfall Project Shiny app"
   git push origin main
   ```

2. **Configure GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to Settings > Pages
   - Under "Source", select "Deploy from a branch"
   - Choose "main" branch and "/docs" folder
   - Click "Save"

3. **Wait for deployment** (usually takes a few minutes)

## Step 4: Alternative Hosting Options

### Option A: ShinyApps.io (External Hosting)
If you prefer to host on ShinyApps.io:

1. **Deploy to ShinyApps.io**:
   ```r
   library(rsconnect)
   deployApp("wisconsin-rainfall-app", appName = "wisconsin-rainfall-project")
   ```

2. **Update the iframe source** in `wisconsin-rainfall-project.html`:
   ```html
   <iframe 
       src="https://yourusername.shinyapps.io/wisconsin-rainfall-project/" 
       width="100%" 
       height="100%" 
       frameborder="0">
   </iframe>
   ```

### Option B: Custom Server Hosting
If you have your own server:

1. **Deploy your Shiny app** to your server
2. **Update the iframe source** to point to your server URL
3. **Ensure CORS is properly configured** for iframe embedding

## Step 5: Testing and Troubleshooting

### Test Your Integration
1. Visit your Wisconsin Rainfall Project page
2. Verify the iframe loads correctly
3. Test all interactive features
4. Check on different devices and browsers

### Common Issues and Solutions

**Issue**: Iframe shows "Application temporarily unavailable"
- **Solution**: Check that the `docs/index.html` file exists and is accessible
- **Solution**: Verify GitHub Pages is configured to serve from `/docs`

**Issue**: App loads but doesn't function properly
- **Solution**: Check browser console for JavaScript errors
- **Solution**: Ensure all data files are included in the export

**Issue**: App is too slow to load
- **Solution**: Optimize your data files (compress, subset if needed)
- **Solution**: Consider lazy loading for large datasets

## Step 6: Maintenance

### Updating Your App
1. Make changes to your Shiny app
2. Re-export using shinylive:
   ```r
   shinylive::export(appdir = "wisconsin-rainfall-app", destdir = "docs")
   ```
3. Commit and push changes:
   ```bash
   git add docs/
   git commit -m "Update Wisconsin Rainfall Project app"
   git push origin main
   ```

### Monitoring
- Check GitHub Pages deployment status
- Monitor app performance and user feedback
- Keep R packages and dependencies updated

## File Structure After Setup
```
her.github.io/
├── docs/                          # GitHub Pages source
│   ├── index.html                 # Your Shiny app
│   ├── app/                       # Shiny app files
│   └── ...                        # Other exported files
├── wisconsin-rainfall-project.html # Your project page
├── projects.html                  # Updated with new link
└── ...                           # Other website files
```

## Support
If you encounter issues:
1. Check the browser console for errors
2. Verify GitHub Pages deployment status
3. Test the app locally first
4. Contact Dr. Daniel Wright (danielb.wright@wisc.edu) for technical support

---

**Note**: The current setup uses Shinylive for optimal GitHub Pages integration. This approach provides the best user experience and eliminates the need for external hosting services.
