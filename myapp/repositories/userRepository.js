
import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';
import OrgRepository from './OrgRepository.js'
import OrganizationUsers from './organization_users.js'
import UserRoleRepo from './userRoleRepository.js';
import RolesRepo from './RoleRepository.js'
class UserRepository extends baseRepository {

    constructor() {
        super('users', db);
        this.orgRepo = new OrgRepository();
        this.orgUser = new OrganizationUsers();
        this.userRole = new UserRoleRepo();
        this.rolesRepo = new RolesRepo();
    }

    async userCreate(data) {
        const connection = await db.getConnection();
        try {
            await connection.beginTransaction();

            const { email, password_hash, name } = data;

            const user = await this.create({ email, password_hash, name }, connection);

            const org = await this.orgRepo.create({ name: "default" }, connection);

            const org_user = await this.orgUser.create({ organization_id: org.id, user_id: user.id }, connection);

            const role = await this.rolesRepo.findByColumnsAndGetId({ col_data: "super_admin", col_name: "name", table_name: "roles" }, connection)

            const org_role_user = await this.userRole.create({ organization_id: org.id, user_id: user.id, role_id: role.id }, connection)




            await connection.commit();

            return { user, org, org_user, org_role_user };
        } catch (err) {
            await connection.rollback();
            throw err;
        } finally {
            connection.release();
        }
    }


}







export default UserRepository;
