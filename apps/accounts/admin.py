from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'name', 'date_joined')
    list_filter = ('email_verified', 'is_marked_for_deletion')
    filter_horizontal = ()
    search_fields = ('email', 'username', 'name')
    readonly_fields = ('id', 'uuid', 'short_uuid', 'last_login', 'date_joined')

    fieldsets = (
        ('General information', {
            'fields': ('email', 'username', 'name'),
            'description': 'General account information'},
         ),
        ('User preferences', {
            'fields': ('profile_image', 'description', 'theme',),
            'description': 'General account information'},
         ),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser'),
            'description': 'Permissions for the account'},
         ),
        ('Email verification', {
            'fields': ('email_verified',),
            'description': 'Account verification parameters'},
         ),
        ('Account deletion', {
            'fields': ('is_marked_for_deletion', 'date_marked_for_deletion'),
            'description': 'Account deletion parameters'},
         ),
        ('Read only properties', {
            'fields': ('id', 'uuid', 'short_uuid', 'date_joined', 'last_login'),
            'description': 'Ready only properties that cannot be modified'},
         ),
        ('Notes', {
            'fields': [],  # Use an empty list as there are no fields
            'description': '''
                <b>Additional properties:</b><br>
                - full_name: Returns the full name of the user (first_name + last_name)<br>
            '''},
         ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        field_type = db_field.get_internal_type()
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field
