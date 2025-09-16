from django.contrib.auth.models import Group

LIST_OF_GROUPS = ["ADMIN", "CLIENT"]

def build_group_list():
    for group in LIST_OF_GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)
        if created:
            print(f"New group named {new_group} created successfully!")
        else:
            print(
                f"We couldn't create a group with name {group}. It seems {group} has already been declared as a group name.")
    return

def isAdmin(user):
    user_groups_queryset = user.groups.all()
    cur_user_groups = [group.name for group in list(user_groups_queryset)]
    if "ADMIN" in cur_user_groups:
        return True
    return False

def isClient(user):
    user_groups_queryset = user.groups.all()
    cur_user_groups = [group.name for group in list(user_groups_queryset)]
    if "CLIENT" in cur_user_groups:
        return True
    return False
