import userService from '../service/userService.js';
import authService from '../service/authService.js';


class AuthController {
    static async signup(req, res) {
        try {
            const result = await userService.UserCreate(req.body);
            res.status(201).json(result);
        } catch (error) {
            const statusCode = error.statusCode || 500;
            res.status(statusCode).json({
                message: error.message || 'An error occurred during signup'
            });
        }
    }

    static async login(req, res) {
        try {
            const result = await authService.login(req.body.email, req.body.password);
            res.status(200).json(result);
        } catch (error) {
            const statusCode = error.statusCode || 500;
            res.status(statusCode).json({
                message: error.message || 'An error occurred during login'
            });
        }
    }

    static async getAllUsers(req, res) {
        try {
            const users = await userService.getAllUsers();
            res.status(200).json(users);
        } catch (error) {
            const statusCode = error.statusCode || 500;
            res.status(statusCode).json({
                message: error.message || 'Failed to fetch users'
            });
        }
    }

    static async getUserById(req, res) {
        try {
            const user = await userService.getUserById(req.params.id);
            res.status(200).json(user);
        } catch (error) {
            const statusCode = error.statusCode || 500;
            res.status(statusCode).json({
                message: error.message || 'Failed to fetch user'
            });
        }
    }

    static async updateUser(req, res) {
        try {
            const result = await userService.updateUser(req.params.id, req.body);
            res.status(200).json(result);
        } catch (error) {
            const statusCode = error.statusCode || 500;
            res.status(statusCode).json({
                message: error.message || 'Failed to update user'
            });
        }
    }

    static async deleteUser(req, res) {
        try {
            const result = await userService.deleteUser(req.params.id);
            res.status(200).json(result);
        } catch (error) {
            const statusCode = error.statusCode || 500;
            res.status(statusCode).json({
                message: error.message || 'Failed to delete user'
            });
        }
    }
}

export default AuthController;


