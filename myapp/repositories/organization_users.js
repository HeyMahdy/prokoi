import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';

class OrganizationUsers extends baseRepository {
    constructor() {
        super("organization_users", db)
    }
}
export default OrganizationUsers;