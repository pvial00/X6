class X6:
   def __init__(self, key):
      self.key = key
      self.mod = 26
      self.rounds = 1
      self.blocksize = 16
      self.keyrounds = 128
      self.keyinit = "AKEYISNOTFIREYEZ"

   def hfunc(self, block):
      block[0] = (block[0] + block[2] + 12) % self.mod
      block[1] = (block[1] + block[14] + 4) % self.mod
      block[2] = (block[2] + block[5] + 13) % self.mod
      block[3] = (block[3] + block[8] + 21) % self.mod
      block[4] = (block[4] + block[1] + 16) % self.mod
      block[5] = (block[5] + block[9] + 2) % self.mod
      block[6] = (block[6] + block[0] + 9) % self.mod
      block[7] = (block[7] + block[15] + 25) % self.mod
      block[8] = (block[8] + block[4] + 20) % self.mod
      block[9] = (block[9] + block[6] + 5) % self.mod
      block[10] = (block[10] + block[7] + 22) % self.mod
      block[11] = (block[11] + block[13] + 3) % self.mod
      block[12] = (block[12] + block[12] + 11) % self.mod
      block[13] = (block[13] + block[10] + 1) % self.mod
      block[14] = (block[14] + block[11] + 17) % self.mod
      block[15] = (block[15] + block[3] + 6) % self.mod
      return block
   
   def hfunc2(self, block):
      block[0] = (block[1] + block[2] + 5) % self.mod
      block[1] = (block[13] + block[14] + 22) % self.mod
      block[2] = (block[6] + block[5] + 20) % self.mod
      block[3] = (block[15] + block[8] + 14) % self.mod
      block[4] = (block[5] + block[1] + 11) % self.mod
      block[5] = (block[6] + block[9] + 17) % self.mod
      block[6] = (block[0] + block[0] + 19) % self.mod
      block[7] = (block[11] + block[15] + 20) % self.mod
      block[8] = (block[9] + block[4] + 23) % self.mod
      block[9] = (block[3] + block[6] + 3) % self.mod
      block[10] = (block[12] + block[7] + 9) % self.mod
      block[11] = (block[14] + block[13] + 4) % self.mod
      block[12] = (block[2] + block[12] + 15) % self.mod
      block[13] = (block[10] + block[10] + 7) % self.mod
      block[14] = (block[8] + block[11] + 13) % self.mod
      block[15] = (block[7] + block[3] + 0) % self.mod
      return block
   
   def keysetup(self, key, nonce):
      h = []
      n = []
      for x in range(self.blocksize):
         h.append(ord(key[x]) - 65)
      for x in range(self.blocksize):
         n.append(ord(nonce[x]) - 65)
      for x, char in enumerate(h):
          h[x] = (char + (ord(self.keyinit[x]) - 65)) % 26
      for x in range(self.keyrounds):
          h = self.hfunc(h)
          h = self.hfunc2(h)
          n = self.hfunc(n)
      for x, char in enumerate(n):
          h[x] = (char + h[x]) % 26
      for x in range(self.keyrounds):
          h = self.hfunc(h)
          h = self.hfunc2(h)
      return h

   def encrypt(self, data, nonce):
      num_blocks = len(data) / 16
      extra = len(data) / 16
      extra_block = 0
      if extra > 0:
          extra_block = 1
      blocks = []
      s = 0
      e = 16
      for x in range(num_blocks + extra_block):
         b = data[s:e]
         block = []
         for n in range(len(b)):
            block.append((ord(b[n]) - 65))
         blocks.append(block)
         s += 16
         e += 16
      ctxt = []
      h = self.keysetup(self.key, nonce)
      for x, block in enumerate(blocks):
         for r in range(self.rounds):
             h = self.hfunc(h)
         for c, char in enumerate(block):
             ctxt.append(chr(((h[c] + char + x) % 26) + 65))
      return "".join(ctxt)
   
   def decrypt(self, data, nonce):
      num_blocks = len(data) / self.blocksize
      extra = len(data) % self.blocksize
      extra_block = 0
      if extra > 0:
          extra_block = 1
      blocks = []
      s = 0
      e = self.blocksize
      for x in range(num_blocks + extra_block):
         b = data[s:e]
         block = []
         for n in range(len(b)):
            block.append((ord(b[n]) - 65))
         blocks.append(block)
         s += self.blocksize
         e += self.blocksize
      ctxt = []
      h = self.keysetup(self.key, nonce)
      for x, block in enumerate(blocks):
         for r in range(self.rounds):
             h = self.hfunc(h)
         for c, char in enumerate(block):
             ctxt.append(chr(((char - h[c] - x) % 26) + 65))
      return "".join(ctxt)
