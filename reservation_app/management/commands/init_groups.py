from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = ""
    GROUPS_NAME_WITH_PERMISSIONS = {
        'scheduler': [
            'view_user',
        ],
    }

    def handle(self, *args, **options):
        for group_name in self.GROUPS_NAME_WITH_PERMISSIONS:
            group, created = Group.objects.update_or_create(name=group_name)
            self.stdout.write(self.style.SUCCESS('- Successfully added group %s:' % group_name))
            for permission_codename in self.GROUPS_NAME_WITH_PERMISSIONS[group_name]:
                try:
                    permission = Permission.objects.get(codename=permission_codename)
                    self.stdout.write(self.style.SUCCESS(
                        '\t- Successfully added permission %s to group %s' % (permission_codename, group_name)))
                except Permission.DoesNotExist as ex:
                    raise CommandError("- Permissions %s doesn't exist." % permission_codename)
                group.permissions.add(permission)
        self.stdout.write(self.style.SUCCESS('- Successfully groups created and its permissions added.'))
