from datetime import datetime, timedelta, timezone



class PermissionHandler:
    def __init__(self, permission_lifetime_in_minute=30):
        self.containers = dict()
        self.permission_lifetime_in_minute = permission_lifetime_in_minute
    
    def set_perm(self, session_id, shared_object):
        self.containers[session_id]: set =                                      \
            self.containers.get(session_id, set())                              \
            |                                                                  \
            {(
                shared_object, 
                datetime.now(tz=timezone.utc) + timedelta(minutes=self.permission_lifetime_in_minute)
            )}
    
    def check_perm(self, session_id, target_object):
        corr_container = self.containers.get(session_id, set())
        corr_container = self._perm_expire_check(corr_container)
        self.containers[session_id] = corr_container
        
        # print(f"\n  {tuple( obj for obj, dt in corr_container) = }\n")
        if target_object in tuple( obj for obj, dt in corr_container):
            return True
        return False
    
    def _perm_expire_check(self, container:set):
        # print(f"\n  running _perm_expire_check, target {container = }\n")
        rm = []
        for obj_dt in container:
            _, dt = obj_dt
            if datetime.now(tz=timezone.utc) > dt:
                # print(f"    remove {obj_dt}")
                rm.append(obj_dt)
        for obj_dt in rm:
            container.remove(obj_dt)
        # print(f"\n  returning {container = }\n")
        return container
    