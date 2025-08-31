import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import UserRepository from '../repositories/userRepository.js'
const userRepository = new UserRepository();

const JWT_SECRET = 'your-secret-key';

class AuthService {
    async login(email, password) {
        try {
            // Find user
            const user = await userRepository.findByEmail(email);

            if (!user) {
                throw new Error('Invalid email or password');
            }

            // Verify password
            const isValidPassword = await bcrypt.compare(password, user.password_hash);
            if (!isValidPassword) {
                throw new Error('Invalid email or password');
            }
            // Generate JWT token
            const token = jwt.sign(
                {
                    userId: user.id,
                    email: user.email
                },
                JWT_SECRET,
                { expiresIn: '24h' }
            );

            return {
                user: {
                    id: user.id,
                    email: user.email,
                },
                token
            };
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async verifyToken(token) {
        try {
            const decoded = jwt.verify(token, JWT_SECRET);
            return decoded;
        } catch (error) {
            console.error('Token verification error:', error);
            throw new Error('Invalid token');
        }
    }

    async getCurrentUser(userId) {
        try {
            const user = await userRepository.findById(userId)

            if (!user) {
                throw new Error('User not found');
            }

            return user;
        } catch (error) {
            console.error('Get current user error:', error);
            throw error;
        }
    }
}

export default new AuthService(); 