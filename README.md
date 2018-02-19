# X6
*** Disclaimer - This cipher is meant for entertainment and educational purposes
 only and should not be used to actually provide good security  
Experimental A-Z Stream Cipher

h[] state can be recovered with only knowing 6 characters of the plaintext and the rest of the ciphertext can be recovered using the h[] state.  Attack was successfully carried about by rgov.

# Class usage:
X6().encrypt(data, key, nonce)  
X6().decrypt(data, key, nonce)  

# Script usage:
python x6crypt.py encrypt/decrypt input file output file key
