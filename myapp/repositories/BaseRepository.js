// repositories/baseRepository.js
class BaseRepository {
    constructor(tableName, db) {
        this.table = tableName;
        this.db = db;
    }

    async findAll() {
        const [rows] = await this.db.promise().query(`SELECT * FROM ${this.table}`);
        return rows;
    }

    async findById(id) {
        const [rows] = await this.db.promise().query(
            `SELECT * FROM ${this.table} WHERE id = ?`,
            [id]
        );
        return rows[0] || null;
    }

    async findByEmail(email) {
        try {
            const [rows] = await this.db.promise().query(
                `SELECT * FROM ${this.table} WHERE email = ?`,
                [email]
            );
            return rows[0] || null;
        }
        catch (error) {
            console.error('Repository: Find by email error:', error);
            throw error;
        }

    }

    async findByColumnsAndGetId(col_data, col_name, table_name) {
        try {
            const [rows] = await this.db.promise().query(
                `SELECT * FROM ${table_name} WHERE ${col_name} = ?`,
                [col_data]
            );
            if (rows.length === 0) return null;  // no row found
            return { id: rows[0].id };           // return id of first matching row
        }
        catch (error) {
            console.error('Repository: Find by column error:', error);
            throw error;
        }
    }

    async create(data) {
        const keys = Object.keys(data).join(',');
        const values = Object.values(data);
        const placeholders = values.map(() => '?').join(',');

        const [result] = await this.db.promise().query(
            `INSERT INTO ${this.table} (${keys}) VALUES (${placeholders})`,
            values
        );

        return { id: result.insertId, ...data };
    }


}

export default BaseRepository;
