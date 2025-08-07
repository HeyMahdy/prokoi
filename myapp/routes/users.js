const express = require('express');
const router = express.Router();
const UsersController = require('../controllers/usersController');

router.get('/', UsersController.getAllUsers);
router.post('/', UsersController.CreateUser);

module.exports = router;