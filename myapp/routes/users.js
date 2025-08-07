import express from 'express';
import AuthController from '../controllers/usersController.js';

const router = express.Router();

// Auth routes
router.post('/signup', AuthController.signup);
router.post('/login', AuthController.login);

// CRUD routes
router.get('/', AuthController.getAllUsers);           // GET /api/users
router.get('/:id', AuthController.getUserById);       // GET /api/users/:id
router.put('/:id', AuthController.updateUser);        // PUT /api/users/:id
router.delete('/:id', AuthController.deleteUser);     // DELETE /api/users/:id

export default router;