class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """
        Point all read operations to the appropriate database.
        """
        if model._meta.app_label == 'api_users':
            return 'default'
        elif model._meta.app_label == 'Projects':
            return 'db2'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all write operations to the appropriate database.
        """
        if model._meta.app_label == 'api_users':
            return 'default'
        elif model._meta.app_label == 'Projects':
            return 'db2'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if a model in app1 is involved.
        """
        if obj1._meta.app_label == 'api_users' or obj2._meta.app_label == 'api_users':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure all migrations occur on the correct database.
        """
        if app_label == 'api_users':
            return db == 'default'
        elif app_label == 'Projects':
            return db == 'db2'
        return None
