from pycube import CubeKDF, DataNormalizer, CubeRandom
from X6 import X6, X6KDF
import sys, select, getpass, os, time, getopt

try:
    mode = sys.argv[1]
except IndexError as ier:
    print "Error: Did you forget encrypt/decrypt?"
    sys.exit(1)

input_filename = sys.argv[2]
output_filename = sys.argv[3]

try:
    infile = open(input_filename, "r")
except IOError as ier:
    print "Input file not found."
    sys.exit(1)

try:
    outfile = open(output_filename, "w")
except IOError as ier:
    print "Output file not found."
    sys.exit(1)

try:
    key = sys.argv[4]
except IndexError as ier:
    key = getpass.getpass("Enter key: ")

start = time.time()
buf = infile.read()
infile.close()
key = X6KDF().genkey(key)
data = DataNormalizer().normalize(buf)

if mode == "encrypt":
    nonce = CubeRandom().random(16)
    c = X6().encrypt(data, key, nonce)
    outfile.write(nonce+c)
elif mode == "decrypt":
    nonce = data[:16]
    msg = data[16:]
    plain_text = X6().decrypt(msg, key, nonce)
    outfile.write(plain_text)
outfile.close()

end = time.time() - start
bps = len(data) / end
sys.stdout.write("Completed in "+str(end)+" seconds\n")
sys.stdout.write(str(bps)+" bytes per second.\n")
