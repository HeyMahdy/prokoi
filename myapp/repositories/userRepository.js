
import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';


class UserRepository extends baseRepository {

    constructor() {
        super('user', db);
    }

    async OrgCreate(data) {
        const { name, organization_name } = data;  // 'name' is the org owner

        // Values array in the same order as placeholders
        const values = [organization_name, name];

        // Use placeholders `?` to safely insert data
        const [result] = await this.db.promise().query(
            `INSERT INTO organizations (organization_name, organization_owner) VALUES (?, ?)`,
            values
        );



        // Return a friendly object including the new ID
        return {
            id: result.insertId,
            organization_name: organization_name,
            organization_owner: name
        };

    }



    async UserCreate(data) {
        const { email, password, name, organization_name } = data;

        // ✅ Call findByColumns from the parent class
        const orgId = await this.findByColumnsAndGetId(organization_name, 'organization_name', 'organizations');
        if (!orgId) {
            throw new Error('org dos not  exists');
        }

        const user = await this.create({ email, password, name, organization_id: orgId });

        return user;

    }





}







export default UserRepository;
