const { V4 } = require('paseto');
const crypto = require('crypto');

/**
 * PASETO (Platform-Agnostic Security Tokens) for JavaScript
 * --------------------------------------------------------
 * Documentation: https://github.com/panva/paseto
 * 
 * Installation:
 *      npm install paseto
 */

// --- 1. SYMMETRIC ENCRYPTION (v4.local) ---
async function demoSymmetric() {
    console.log("--- JS Symmetric (v4.local) Demo ---");
    
    // 32-byte secret key (represented as a Buffer or Uint8Array)
    const secretKey = crypto.randomBytes(32);
    
    // Payload
    const payload = {
        sub: 'user_123',
        name: 'Nabin Hamal',
        iat: new Date().toISOString(),
    };
    
    // 1. Issue Token
    const token = await V4.encrypt(payload, secretKey);
    console.log(`Issued Token: ${token.substring(0, 40)}...`);
    
    // 2. Decrypt
    const decrypted = await V4.decrypt(token, secretKey);
    console.log(`Decrypted Payload:`, decrypted);
    console.log("\n");
}

// --- 2. ASYMMETRIC SIGNATURES (v4.public) ---
async function demoAsymmetric() {
    console.log("--- JS Asymmetric (v4.public) Demo ---");
    
    // Generate Ed25519 Key Pair
    const { privateKey, publicKey } = await V4.generateKey('public');
    
    // Payload
    const payload = {
        sub: 'admin_456',
        role: 'admin',
    };
    
    // 1. Sign
    const token = await V4.sign(payload, privateKey);
    console.log(`Signed Token: ${token.substring(0, 40)}...`);
    
    // 2. Verify
    const verified = await V4.verify(token, publicKey);
    console.log(`Verified Payload:`, verified);
    console.log("\n");
}

// Run Demos
(async () => {
    try {
        await demoSymmetric();
        await demoAsymmetric();
    } catch (err) {
        if (err.code === 'MODULE_NOT_FOUND') {
            console.error("Error: 'paseto' package not found. Please run 'npm install paseto'");
        } else {
            console.error("An error occurred:", err);
        }
    }
})();
