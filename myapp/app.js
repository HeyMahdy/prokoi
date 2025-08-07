import express from 'express';
import { swaggerUi, swaggerSpec } from './config/swagger.js'
const app = express();
import usersRoutes from './routes/users.js';
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.use(express.json());
app.use('/auth', usersRoutes);

const PORT = 8000;
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
