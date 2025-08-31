
import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';
import OrgRepository from './OrgRepository.js'
import OrganizationUsers from './organization_users.js'

class UserRepository extends baseRepository {

    constructor() {
        super('users', db);
        this.orgRepo = new OrgRepository();
        this.orgUser = new OrganizationUsers();
    }

    async userCreate(data) {
        const connection = await db.getConnection();
        try {
            await connection.beginTransaction();

            const { email, password_hash, name } = data;

            const user = await this.create({ email, password_hash, name }, connection);

            const org = await this.orgRepo.create({ name: "default" }, connection);

            const org_user = await this.orgUser.create({ organization_id: org.id, user_id: user.id }, connection);

            await connection.commit();

            return { user, org, org_user };
        } catch (err) {
            await connection.rollback();
            throw err;
        } finally {
            connection.release();
        }
    }


}







export default UserRepository;
