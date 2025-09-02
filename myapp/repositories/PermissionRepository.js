import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';

class PermissionRepo extends baseRepository {
    constructor() {
        super("permissions", db)
    }
}
export default PermissionRepo;