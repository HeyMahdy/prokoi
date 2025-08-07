const db = require('../db/connection');
const baseRepository = require('./BaseRepository')


class UserRepository extends baseRepository {

    constructor() {
        super('users', db);
    }

}

module.exports = new UserRepository();
