# class TutoriasRouter:
#
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'sysacad':
#             return 'SYSACAD'
#         if model._meta.app_label == 'default':
#             return 'TUTORIAS_DATOS'
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'tutorias':
#             return 'TUTORIAS_DATOS'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         if obj1._meta.app_label == 'sysacad' or \
#            obj2._meta.app_label == 'default':
#            return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label == 'sysacad':
#             return db == 'SYSACAD'
#         elif app_label == 'tutorias':
#             return db == 'TUTORIAS_DATOS'
#         return None
#


def decide_on_model(model):
    """Small helper function to pipe all DB operations of a worlddata model to the world_data DB"""
    return 'sysacad' if model._meta.app_label == 'sysacad' else None


class TutoriasRouter:
    """
    Implements a database router so that:

    * Django related data - DB alias `default` - MySQL DB `world_django`
    * Legacy "world" database data (everything "non-Django") - DB alias `world_data` - MySQL DB `world`
    """
    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    # def db_for_write(self, model, **hints):
    #     return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the worlddata app
        if obj1._meta.app_label == 'sysacad' and obj2._meta.app_label == 'sysacad':
            return True
        # Allow if neither is part of worlddata app
        elif 'sysacad' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # allow migrations on the "default" (django related data) DB
        if db == 'default' and app_label != 'sysacad':
            return True

        # allow migrations on the legacy database too:
        # this will enable to actually alter the database schema of the legacy DB!

        # if db == 'sysacad' and app_label == "sysacad":
        #    return True

        return False