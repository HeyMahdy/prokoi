import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';

class OrgRepository extends baseRepository {
    constructor() {
        super('organizations', db);   // binds this repo to the org table
    }
}

export default OrgRepository;