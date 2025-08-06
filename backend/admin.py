"""
This file configures the administrative interface for the application using SQLAdmin.

It defines how the database models (Zone, Fare) are presented and managed
in the web-based admin panel, controlling list views, creation/edit forms,
and display names.
"""

from sqladmin import ModelView
from .models import Zone, Fare # Use a relative import for models within your package


class ZoneAdmin(ModelView, model=Zone):
    """
    Defines the configuration for the Zone model in the admin panel.
    This class controls how Zone objects are displayed and edited.
    """

    # --- Display Configuration ---
    # These attributes control how the model is identified in the admin UI sidebar.
    name = "Zone"
    name_plural = "Zones"
    icon = "fa-solid fa-map-marker-alt"  # A FontAwesome icon for the navigation menu.

    # --- List View Configuration ---
    # 'column_list' specifies which columns of the Zone table are displayed
    # in the main list view at `/admin/zone/list`.
    column_list = [Zone.id, Zone.name]
    
    # --- Form Configuration ---
    # 'form_columns' specifies which fields are available to edit on the
    # "Create" and "Edit" forms for a Zone.
    form_columns = [Zone.name]
    
    # --- Naming and Labels ---
    # 'column_labels' provides custom, user-friendly names for the columns,
    # overriding the default database column names.
    column_labels = {
        Zone.name: "Zone Name"
    }


class FareAdmin(ModelView, model=Fare):
    """
    Defines the configuration for the Fare model in the admin panel.
    This class controls how Fare objects are displayed and edited.
    """

    # --- Display Configuration ---
    name = "Fare"
    name_plural = "Fares"
    icon = "fa-solid fa-dollar-sign"

    # --- List View Configuration ---
    # Here, we use the SQLAlchemy relationship attributes (e.g., Fare.source_zone)
    # instead of the raw foreign key IDs (e.g., Fare.source_id). This allows
    # SQLAdmin to display the human-readable name of the related Zone object,
    # thanks to the `__str__` method we defined in the Zone model.
    column_list = [Fare.id, Fare.source_zone, Fare.destination_zone, Fare.price]

    # --- Form Configuration ---
    # Similarly, using the relationship attributes here tells SQLAdmin to
    # automatically render them as convenient dropdown select boxes,
    # populated with all available Zones.
    form_columns = [Fare.source_zone, Fare.destination_zone, Fare.price]

    # --- Naming and Labels ---
    # Provides user-friendly labels for better readability in the admin panel.
    column_labels = {
        Fare.source_zone: "Source Zone",
        Fare.destination_zone: "Destination Zone",
        Fare.price: "Fare Price"
    }