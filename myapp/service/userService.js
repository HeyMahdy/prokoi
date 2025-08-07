
const userRepo = require('../repositories/userRepository')

const createUser = async (name, email) => {
    const exists = await userRepo.findByEmail(email);
    if (exists) {
        throw new Error('DUPLICATE_EMAIL');
    }
    const user = await userRepo.create({ name, email });
    return user;
};


const getAllUsers = async () => {
    return await userRepo.findAll();
};

module.exports = {
    getAllUsers,
    createUser
};