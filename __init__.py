keyinit = "MYVOICECANSINGTO"

def charstonum(chars):
    nums = []
    for char in chars:
       nums.append(ord(char) - 65)
    return nums

def numstochars(nums):
    chars = []
    for num in nums:
        chars.append(chr(num + 65))
    return chars

def blockdata(data, padding=False, blocksize=16):
   num_blocks = len(data) / blocksize
   extra = len(data) % blocksize
   extra_block = 0
   padchar = 25
   if extra > 0:
      extra_block = 1
   blocks = []
   s = 0
   e = blocksize
   for x in range(num_blocks + extra_block):
      b = data[s:e]
      block = []
      for n in range(len(b)):
         block.append((ord(b[n]) - 65))
      if padding == True and extra > 0 and x == ((num_blocks + extra_block) - 1):
         if len(data) < blocksize:
             extra = blocksize - len(data)
         for e in range(extra):
             block.append(padchar)
      blocks.append(block)
      s += blocksize
      e += blocksize
   return blocks

def hfunc(block, counter=0,  mod=26):
   block[0] = (block[2] + block[1] + block[4] + 14) % mod
   block[1] = (block[0] + block[12] + block[14] + 5) % mod
   block[2] = (block[1] + block[3] + block[3] + 1) % mod
   block[3] = (block[6] + block[5] + block[6] + 19) % mod
   block[4] = (block[7] + block[2] + block[8] + 13) % mod
   block[5] = (block[12] + block[10] + block[0] + 17) % mod
   block[6] = (block[5] + block[8] + block[11] + 24) % mod
   block[7] = (block[13] + block[6] + block[15] + 23) % mod
   block[8] = (block[15] + block[4] + block[12] + 0) % mod
   block[9] = (block[9] + block[15] + block[5] + 4) % mod
   block[10] = (block[14] + block[13] + block[1] + 23) % mod
   block[11] = (block[3] + block[11] + block[10] + 8) % mod
   block[12] = (block[4] + block[7] + block[13] + 25 + counter) % mod
   block[13] = (block[10] + block[0] + block[9] + 20) % mod
   block[14] = (block[8] + block[14] + block[2] + 15) % mod
   block[15] = (block[11] + block[9] + block[7] + 7) % mod
   return block
   
def hfunc2(block, mod=26):
   block[0] = (block[5] + block[12]) % mod
   block[1] = (block[2] + block[4]) % mod
   block[2] = (block[12] + block[2]) % mod
   block[3] = (block[8] + block[9]) % mod
   block[4] = (block[11] + block[15]) % mod
   block[5] = (block[4] + block[6]) % mod
   block[6] = (block[7] + block[3]) % mod
   block[7] = (block[1] + block[7]) % mod
   block[8] = (block[15] + block[11]) % mod
   block[9] = (block[0] + block[13]) % mod
   block[10] = (block[14] + block[1]) % mod
   block[11] = (block[6] + block[7]) % mod
   block[12] = (block[9] + block[14]) % mod
   block[13] = (block[3] + block[0]) % mod
   block[14] = (block[10] + block[8]) % mod
   block[15] = (block[7] + block[10]) % mod
   return block

def keysetup(key, nonce, blocksize=16, keyrounds=128):
   h = []
   n = []
   for x in range(blocksize):
      h.append(ord(key[x]) - 65)
   for x in range(blocksize):
      n.append(ord(nonce[x]) - 65)
   for x, char in enumerate(h):
       h[x] = (char + (ord(keyinit[x]) - 65)) % 26
   for x in range(keyrounds):
       h  = hfunc(h)
       h = hfunc2(h)
   for x, char in enumerate(n):
       h[x] = (char + h[x]) % 26
   for x in range(keyrounds):
       h  = hfunc(h)
       h = hfunc2(h)
   return h

class X6:

   def encrypt(self, data, key, nonce):
      blocks = blockdata(data)
      ctxt = []
      h = keysetup(key, nonce)
      counter = 0
      for b, block in enumerate(blocks):
         h = hfunc(h, counter)
         h = hfunc2(h)
         for c, char in enumerate(block):
             ctxt.append(chr(((h[c] + char) % 26) + 65))
             counter = (counter + 1) % 26
      return "".join(ctxt)
   
   def decrypt(self, data, key, nonce):
      blocks = blockdata(data)
      ctxt = []
      h = keysetup(key, nonce)
      counter = 0
      for b, block in enumerate(blocks):
         h = hfunc(h, counter)
         h = hfunc2(h)
         for c, char in enumerate(block):
             ctxt.append(chr(((char - h[c]) % 26) + 65))
             counter = (counter + 1) % 26
      return "".join(ctxt)

class X6Hash:
  blocksize = 16
  rounds = 1

  def digest(self, data, key=""):
      blocks = blockdata(data, padding=True)
      last = [0] * self.blocksize 
      blockhashes = []
      for block in blocks:
          for r in range(self.rounds):
              h = hfunc(block)
              h = hfunc2(h)
              for c, char in enumerate(last):
                  h[c] = (h[c] + char + c) % 26
          blockhashes.append(h)
          last = h
      for block in blockhashes:
          for c, char in enumerate(block):
              h[c] = (char + h[c]) % 26
      h = keysetup(numstochars(h), numstochars(last))
      return "".join(numstochars(h))

class X6KDF:
    def __init__(self, iterations=100):
        self.iterations = iterations

    def genkey(self, key):
        h = key
        for i in range(self.iterations):
            h = X6Hash().digest(h)
        return h
