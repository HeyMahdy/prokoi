// repositories/baseRepository.js
class BaseRepository {
    constructor(tableName, db) {
        this.table = tableName;
        this.db = db;
    }

    // -----------------------------
    // Internal query helper
    // -----------------------------
    async query(sql, params = [], connection = null) {
        if (connection) {
            const [rows] = await connection.query(sql, params);
            return rows;
        } else {
            const [rows] = await this.db.query(sql, params);
            return rows;
        }
    }

    // -----------------------------
    // CRUD operations
    // -----------------------------
    async findAll(connection = null) {
        return this.query(`SELECT * FROM ${this.table}`, [], connection);
    }

    async findById(id, connection = null) {
        const rows = await this.query(
            `SELECT * FROM ${this.table} WHERE id = ?`,
            [id],
            connection
        );
        return rows[0] || null;
    }

    async findByEmail(email, connection = null) {
        try {
            const rows = await this.query(
                `SELECT * FROM ${this.table} WHERE email = ?`,
                [email],
                connection
            );
            return rows[0] || null;
        }
        catch (error) {
            console.error('Repository: Find by email error:', error);
            throw error;
        }
    }

    async findByColumnsAndGetId(col_data, col_name, table_name, connection = null) {
        try {
            const rows = await this.query(
                `SELECT * FROM ${table_name} WHERE ${col_name} = ?`,
                [col_data],
                connection
            );
            if (rows.length === 0) return null;
            return { id: rows[0].id };
        }
        catch (error) {
            console.error('Repository: Find by column error:', error);
            throw error;
        }
    }

    async create(data, connection = null) {
        const keys = Object.keys(data).join(',');
        const values = Object.values(data);
        const placeholders = values.map(() => '?').join(',');

        const result = await this.query(
            `INSERT INTO ${this.table} (${keys}) VALUES (${placeholders})`,
            values,
            connection
        );

        return { id: result.insertId, ...data };
    }

    async updateById(id, data, connection = null) {
        const keys = Object.keys(data);
        const values = Object.values(data);
        const setClause = keys.map(key => `${key} = ?`).join(', ');

        const result = await this.query(
            `UPDATE ${this.table} SET ${setClause} WHERE id = ?`,
            [...values, id],
            connection
        );

        return result.affectedRows > 0;
    }

    async updateByColumn(columnName, columnValue, data, connection = null) {
        const keys = Object.keys(data);
        const values = Object.values(data);
        const setClause = keys.map(key => `${key} = ?`).join(', ');

        const result = await this.query(
            `UPDATE ${this.table} SET ${setClause} WHERE ${columnName} = ?`,
            [...values, columnValue],
            connection
        );

        return result.affectedRows > 0;
    }

    async deleteById(id, connection = null) {
        const result = await this.query(
            `DELETE FROM ${this.table} WHERE id = ?`,
            [id],
            connection
        );
        return result.affectedRows > 0;
    }
}

export default BaseRepository;
