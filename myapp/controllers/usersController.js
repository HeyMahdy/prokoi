
const userService = require('../service/userService');

const getAllUsers = async (req, res) => {
    try {
        const users = await userService.getAllUsers();
        res.json(users);
    } catch (err) {
        res.status(500).send('Server error');
    }
};

const CreateUser = async (req, res) => {
    const { name, email } = req.body;
    try {
        const newUser = await userService.createUser(name, email);
        res.status(201).json(newUser);
    } catch (err) {
        console.error('[CreateUser Error]', err); // 👈 ADD THIS LINE
        if (err.message === 'DUPLICATE_EMAIL') {
            res.status(409).send('Email already exists');
        } else {
            res.status(500).send('Server error');
        }
    }
};

module.exports = {
    getAllUsers,
    CreateUser
};
