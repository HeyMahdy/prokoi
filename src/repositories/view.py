from typing import Any
from src.core.database import db


class ViewRepository:

    async def can_view_workspace(self,workspace_id: int,user_id) -> bool:
        query_01="""
        select 1
        from team_workspaces tw
        join user_team ut on tw.team_id = ut.team_id
        where tw.workspace_id = %s 
        and ut.user_id = %s
        """
        query_02="""
        SELECT r.name
        FROM roles r
        JOIN user_role ur ON r.id = ur.role_id
        WHERE ur.user_id = %s
        AND r.name IN ('admin', 'super_admin', 'supervisor')
        """
        params_01=[workspace_id,]
        params_02=[user_id,]

        return bool(await db.execute_query(query_02, params_01)
                    or await db.execute_query(query_01, params_02))




        

