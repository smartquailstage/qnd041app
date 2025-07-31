# agenda/sites.py
from unfold.sites import UnfoldAdminSite
from django.urls import path, include

class CustomAdminSite(UnfoldAdminSite):
    def get_urls(self):
        # Get the default URLs from the base class
        urls = super().get_urls()
        
        # Define custom admin URLs
        custom_urls = [
            path("", include("agenda.urls_admin")),  # Custom URLs for admin site
        ]
        
        # Return the custom URLs followed by the default ones
        return custom_urls + urls

# Instantiate the custom admin site with the correct name
custom_admin_site = CustomAdminSite(name="admin")
