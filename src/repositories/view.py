from typing import Any
from src.core.database import db


class ViewRepository:

    async def can_view_workspace(self,workspace_id: int,user_id):
        query_01="""
        select 1
        from team_workspaces tw
        join user_team ut on tw.team_id = ut.team_id
        where tw.workspace_id = %s 
        and ut.user_id = %s
        """
        query_02="""
        SELECT 1
        FROM roles r
        JOIN user_role ur ON r.id = ur.role_id
        WHERE ur.user_id = %s
        AND r.name IN ('admin', 'super_admin', 'supervisor')
        """
        params_01=[workspace_id,user_id]
        params_02=[user_id,]
        try:
          f1 = await db.execute_query(query_01, params_01)
          f2 = await db.execute_query(query_02, params_02)
          return bool(f1 or f2)
        except Exception as e:
            print("error in the query")


    async def can_view_workspace_projects(self,project_id: int,user_id: int) -> bool:
        query_01 = """ \
                   select 1 \
                   from project_teams pt \
                            join user_team ut on pt.team_id = ut.team_id \
                   where tw.project_id = %s \
                     and ut.user_id = %s \
                 """
        query_02 = """ \
                   SELECT r.name \
                   FROM roles r \
                            JOIN user_role ur ON r.id = ur.role_id \
                   WHERE ur.user_id = %s \
                     AND r.name IN ('admin', 'super_admin', 'supervisor') \
                 """
        params_01 = [project_id, ]
        params_02 = [user_id, ]

        return bool(await db.execute_query(query_02, params_01)
                    or await db.execute_query(query_01, params_02))




        

