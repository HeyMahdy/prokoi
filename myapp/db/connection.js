import mysql from 'mysql2/promise';
import dotenv from 'dotenv';
// Create a pool (recommended for production + transactions)
dotenv.config({ path: "./myapp/.env" });
console.log(process.env.DB_HOST)
const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

export default db;