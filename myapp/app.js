import express from 'express';
import { swaggerUi, swaggerSpec } from './config/swagger.js'
import cors from 'cors';
const app = express();
import usersRoutes from './routes/users.js';


app.use(cors({
    origin: '*', // Allow all origins
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
    credentials: true
}));
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.use(express.json());
app.use('/auth', usersRoutes);

const PORT = 8000;
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
