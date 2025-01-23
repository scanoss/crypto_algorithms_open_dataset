const crypto = require("crypto");

// MD5 hashing function
function calculateMD5(text) {
  const md5Hash = crypto.createHash("md5");
  md5Hash.update(text);
  return md5Hash.digest("hex");
}

// SHA256 hashing
function calculateSHA256(text) {
  const sha256Hash = crypto.createHash("sha256");
  sha256Hash.update(text);
  return sha256Hash.digest("hex");
}

// AES encryption
function aesEncrypt(text, key) {
  const cipher = crypto.createCipheriv("aes-256-cbc", key, Buffer.alloc(16, 0));
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  return encrypted;
}

// Blowfish encryption
function blowfishEncrypt(text, key) {
  const cipher = crypto.createCipheriv("bf-cbc", key, Buffer.alloc(8, 0));
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  return encrypted;
}

// Example usage
const text = "Hello, World!";
const key = crypto.randomBytes(32);
const bfKey = crypto.randomBytes(16);

console.log("MD5:", calculateMD5(text));
console.log("SHA256:", calculateSHA256(text));
console.log("AES Encrypted:", aesEncrypt(text, key));
console.log("Blowfish Encrypted:", blowfishEncrypt(text, bfKey));
