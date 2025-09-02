import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';

class UserRoleRepo extends baseRepository {
    constructor() {
        super("user_role", db)
    }
}
export default UserRoleRepo;