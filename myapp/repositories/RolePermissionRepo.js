import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';

class RolePermissionRepo extends baseRepository {
    constructor() {
        super("role_permissions", db)
    }
}
export default RolePermissionRepo;