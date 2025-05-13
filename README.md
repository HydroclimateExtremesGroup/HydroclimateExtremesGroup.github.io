# Hydroclimate Extremes Research Group Website

This repository contains the source code for the Hydroclimate Extremes Research Group website. The website is built using HTML5, CSS3, and JavaScript, and is hosted on GitHub Pages.

## Structure

The website consists of the following main sections:
- Home
- Research Areas
- Team Members
- Publications
- Contact Information

## File Structure

```
.
├── index.html          # Main HTML file
├── css/
│   └── style.css      # Main stylesheet
├── js/
│   └── main.js        # JavaScript functionality
└── images/            # Directory for images
```

## Customization

### Adding Team Members

To add a team member, edit the `index.html` file and add a new team member card in the team section:

```html
<div class="team-member">
    <div class="member-photo">
        <img src="images/member-name.jpg" alt="Member Name">
    </div>
    <h3>Member Name</h3>
    <p>Member's role and brief bio</p>
</div>
```

### Adding Publications

To add a publication, add a new publication entry in the publications section:

```html
<div class="publication">
    <p class="publication-year">YEAR</p>
    <p class="publication-title">Publication Title</p>
    <p class="publication-authors">Authors</p>
    <p class="publication-journal">Journal Name</p>
</div>
```

### Updating Contact Information

Update the contact information in the contact section of `index.html`:

```html
<div class="contact-info">
    <p><i class="fas fa-envelope"></i> Email: your.email@institution.edu</p>
    <p><i class="fas fa-location-dot"></i> Location: Your Institution</p>
</div>
```

## Development

1. Clone the repository
2. Make your changes
3. Test locally
4. Commit and push to GitHub
5. The website will automatically update through GitHub Pages

## Maintenance

- Regularly update the publications section with new research
- Keep team member information current
- Update contact information as needed
- Ensure all links are working
- Optimize images before adding them to the site

## License

This website is maintained by the Hydroclimate Extremes Research Group. All rights reserved. 