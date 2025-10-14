from src.repositories.view import ViewRepository

class View:
    def __init__(self):
        self.viewRepo = ViewRepository()

    async def can_view_workspace(self,workspace_id: int,user_id:int) -> bool:
        try:
            result = await self.viewRepo.can_view_workspace(workspace_id,user_id)
            return result
        except Exception as e:
            raise e

    async def can_view_workspace_projects(self,project_id: int,user_id: int) -> bool:
        try:
            result = await self.viewRepo.can_view_workspace_projects(project_id,user_id)
            return result
        except Exception as e:
            raise e

