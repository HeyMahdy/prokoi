



class WorkspaceService {
	async WorkspaceCreate(data) {
		try {
			const { name, organization_id, user_id, team_id = null } = data;
			console.log('Workspace create data received:', data);

			// Validate input
			if (!name || !organization_id || !user_id) {
				const error = new Error('name, organization_id, user_id are required');
				error.statusCode = 400;
				throw error;
			}

			// Ensure creator is org member
			const orgMember = await orgUserRepository.findByOrgAndUser(organization_id, user_id);
			if (!orgMember) {
				const error = new Error('User is not a member of the organization');
				error.statusCode = 403;
				throw error;
			}

			// Optional: validate team belongs to org
			if (team_id !== null) {
				const team = await teamRepository.findTeamByIdAndOrg(team_id, organization_id);
				if (!team) {
					const error = new Error('Team does not belong to the organization');
					error.statusCode = 400;
					throw error;
				}
			}

			// Ensure unique (organization_id, name)
			const existingWs = await workspaceRepository.findByOrgAndName(organization_id, name);
			if (existingWs) {
				const error = new Error('A workspace with this name already exists in the organization');
				error.statusCode = 409;
				throw error;
			}

			// Create workspace (no transaction)
			const workspace = await workspaceRepository.create({
				name,
				user_id,
				team_id, // nullable
				organization_id
			});

			// Add creator as workspace owner
			await workspaceRepository.addUserToWorkspace({
				workspace_id: workspace.id,
				user_id,
				role: 'owner'
			});

			// Link team (M2M) if provided
			if (team_id !== null) {
				await workspaceRepository.linkTeam({
					team_id,
					workspace_id: workspace.id
				});
			}

			console.log('Workspace created successfully:', workspace);
			return {
				message: 'Workspace created successfully',
				workspace
			};
		} catch (error) {
			// Handle unique constraint error code if surfaced from DB
			if (error.code === 'ER_DUP_ENTRY') {
				error.statusCode = 409;
				error.message = 'A workspace with this name already exists in the organization';
			}
			console.error('Error in WorkspaceCreate:', error);
			throw error;
		}
	}
}

export default new WorkspaceService();