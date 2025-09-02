import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';

class RolesRepo extends baseRepository {
    constructor() {
        super("roles", db)
    }
}
export default RolesRepo;