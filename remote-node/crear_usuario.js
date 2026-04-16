const fs = require('fs');
const path = require('path');
const bcrypt = require('bcrypt');
const otplib = require('otplib');

const USERS_FILE = path.join(__dirname, 'data', 'users.json');

// Crear la carpeta data si no existe
if (!fs.existsSync(path.join(__dirname, 'data'))) {
    fs.mkdirSync(path.join(__dirname, 'data'));
}

let users = [];
if (fs.existsSync(USERS_FILE)) {
    users = JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.log("Uso: node crear_usuario.js <username> <password> [--2fa]");
    process.exit(1);
}

const username = args[0];
const password = args[1];
const use2FA = args.includes('--2fa');

const hashedPassword = bcrypt.hashSync(password, 10);
let secret2fa = null;

if (use2FA) {
    secret2fa = otplib.authenticator.generateSecret();
    console.log(`\n==============================================`);
    console.log(`🔐 SE HA HABILITADO 2FA PARA EL USUARIO: ${username}`);
    console.log(`ESCANEA O INGRESA ESTE SECRETO EN GOOGLE AUTHENTICATOR:`);
    console.log(`--->  ${secret2fa}  <---`);
    console.log(`==============================================\n`);
}

// Actualizar o agregar usuario
const userIndex = users.findIndex(u => u.username === username);
if (userIndex >= 0) {
    users[userIndex].password = hashedPassword;
    users[userIndex].totp_secret = secret2fa;
    console.log(`Usuario '${username}' actualizado.`);
} else {
    users.push({ username, password: hashedPassword, totp_secret: secret2fa });
    console.log(`Usuario '${username}' creado exitosamente.`);
}

fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), 'utf8');
console.log("Credenciales guardadas en data/users.json");
