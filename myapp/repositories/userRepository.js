import db from '../db/connection.js';
import baseRepository from './BaseRepository.js';


class UserRepository extends baseRepository {

    constructor() {
        super('user', db);
    }



}

export default UserRepository;
