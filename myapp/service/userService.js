import UserRepository from '../repositories/userRepository.js';
const userRepository = new UserRepository();
import bcrypt from 'bcryptjs';
class UserService {
    async UserCreate(data) {
        try {
            const { email, password, name, organization_name, create = false, is_active } = data;
            console.log('Signup data received:', data);

            // Validate input
            if (!password || !email || !name || !organization_name) {
                const error = new Error('All fields are required');
                error.statusCode = 400;
                throw error;
            }

            // Check if user already exists
            const existingUser = await userRepository.findByEmail(email);
            console.log('Existing user check:', existingUser);
            if (existingUser) {
                const error = new Error('User with this email already exists');
                error.statusCode = 400;
                throw error;
            }

            const hashedPassword = await bcrypt.hash(password, 10);
            console.log('Hashed password:', hashedPassword);

            let user;

            if (create) {
                console.log('Creating new organization...');
                const org = await userRepository.OrgCreate({ name, organization_name });
                console.log('New organization created:', org);

                user = await userRepository.create({
                    email,
                    password: hashedPassword,
                    name,
                    organization_id: org.id,
                    is_active: true
                });
            } else {
                console.log('Joining existing organization...');
                const org = await userRepository.findByColumnsAndGetId(organization_name, 'organization_name', 'organizations');
                if (!org) {
                    throw new Error('Organization does not exist');
                }
                console.log('Organization found:', org);

                user = await userRepository.create({
                    email,
                    password: hashedPassword,
                    name,
                    organization_id: org.id,
                    is_active: false
                });
            }

            console.log('User created successfully:', user);

            return {
                message: 'User created successfully',
                user
            };
        } catch (error) {
            console.error('Error in UserCreate:', error);
            throw error;
        }
    }


    async getAllUsers() {
        try {
            const users = await userRepository.findAll();
            return users;
        } catch (error) {
            console.error('Service: Get all users error:', error);
            const serviceError = new Error('Failed to fetch users');
            serviceError.statusCode = 500;
            throw serviceError;
        }
    }

    async getUserById(id) {
        if (!id) {
            const error = new Error('User ID is required');
            error.statusCode = 400;
            throw error;
        }

        try {
            const user = await userRepository.findById(id);
            if (!user) {
                const error = new Error('User not found');
                error.statusCode = 404;
                throw error;
            }
            return user;
        } catch (error) {
            if (error.statusCode) {
                throw error; // Re-throw custom errors
            }
            console.error('Service: Get user by ID error:', error);
            const serviceError = new Error('Failed to fetch user');
            serviceError.statusCode = 500;
            throw serviceError;
        }
    }

    async updateUser(id, userData) {
        if (!id) {
            const error = new Error('User ID is required');
            error.statusCode = 400;
            throw error;
        }

        if (!userData || Object.keys(userData).length === 0) {
            const error = new Error('Update data is required');
            error.statusCode = 400;
            throw error;
        }

        try {
            // Check if user exists
            const existingUser = await userRepository.findById(id);
            if (!existingUser) {
                const error = new Error('User not found');
                error.statusCode = 404;
                throw error;
            }

            // If email is being updated, check for duplicates
            if (userData.email && userData.email !== existingUser.email) {
                const emailExists = await userRepository.findByEmail(userData.email);
                if (emailExists) {
                    const error = new Error('Email already exists');
                    error.statusCode = 400;
                    throw error;
                }
            }

            const result = await userRepository.update(id, userData);
            return {
                message: 'User updated successfully',
                data: result
            };
        } catch (error) {
            if (error.statusCode) {
                throw error; // Re-throw custom errors
            }
            console.error('Service: Update user error:', error);
            const serviceError = new Error('Failed to update user');
            serviceError.statusCode = 500;
            throw serviceError;
        }
    }

    async deleteUser(id) {
        if (!id) {
            const error = new Error('User ID is required');
            error.statusCode = 400;
            throw error;
        }

        try {
            // Check if user exists
            const existingUser = await userRepository.findById(id);
            if (!existingUser) {
                const error = new Error('User not found');
                error.statusCode = 404;
                throw error;
            }

            const result = await userRepository.delete(id);
            return {
                message: 'User deleted successfully',
                data: result
            };
        } catch (error) {
            if (error.statusCode) {
                throw error; // Re-throw custom errors
            }
            console.error('Service: Delete user error:', error);
            const serviceError = new Error('Failed to delete user');
            serviceError.statusCode = 500;
            throw serviceError;
        }
    }
}

export default new UserService();









