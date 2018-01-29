from random import randint # pretty standard way of generating random stuff
from random import SystemRandom # cryptographically secure way of generating random numbers, uses os.urandom() under the hood

'''main'''
def main():
    choices = ["1", "2", "3", "4"]
    choice = "0"
    while True:  # while loops to continue going through menus until user wants to quit
        while choice not in choices:
            # presents 4 options for the user on what they can do
            print("What would you like to do?")
            print("1. Generate one-time pads")
            print("2. Encrypt a message")
            print("3. Decrypt a message")
            print("4. Quit the program")
            choice = input("Please type 1, 2, 3, or 4 and press Enter : ")

            if choice == "1":  # generate one-time pads (otp), asks user for number of OTPs and max message length
                sheets = int(input("How many one-time pads would you like to generate? : "))
                length = int(input("What will be your maximum message length? : "))
                generate_otp(sheets, length)

            if choice == "2":  # encrypt a message
                while True: # loops until a valid file is entered
                    filename = input("Enter the file name of the OTP you want to use to encrypt your message. "
                                     "Ex: otp0.txt : ")  # gets file name from user
                    try:
                        sheet = load_sheet(filename)  # selects sheet that user wanted
                    except FileNotFoundError:
                        print("File does not exist, try entering a different filename")
                    else:
                        break

                plaintext = get_plain_text()  # gets message from user
                print("Encrypting...")
                ciphertext = encrypt(plaintext, sheet)  # encrypts message
                filename = input("What do you want to name the encrypted file? Be sure to include file extension like .txt : ")  # gets name for encrypted file
                save_file(filename, ciphertext)  # saves encrypted file
                print("File saved, its name is '{}'".format(filename))

            if choice == "3":  # decrypt a message
                while True: #loops until a valid file is entered
                    filename = input("Enter the file name of the OTP you want to use to decrypt your message. "
                                     "Ex: otp0.txt : ")  # gets file name from user
                    try:
                        sheet = load_sheet(filename)  # selects sheet that user wanted
                    except FileNotFoundError:
                        print("File does not exist, try entering a different filename")
                    else:
                        break

                while True: #loops until a valid file is entered
                    filename = input("Enter the name of the file to be decrypted : ")  # gets name of encrypted file
                    try:
                        ciphertext = load_file(filename)  # loads file with encrypted text

                    except FileNotFoundError:
                        print("File does not exist, try entering a different filename")
                    else:
                        break

                plaintext = decrypt(ciphertext, sheet)  # decrypts message
                print("Decrypting... ")
                print("Decrypted message : \n {}".format(plaintext))

            if choice == "4":  # exit program
                exit()
            choice = "0"  # sets choice back to 0 so loop continues



ALPHABET = "abcdefghijklmnopqrstuvwxyz"

'''otp stands for one-time pad, an otp is a string of random numbers that are shared and each letter
in the message is shifted by the corresponding number in the otp. Sheets is how many files will be created with numbers
inside. Length is the amount of numbers in each sheet'''
def generate_otp(sheets, length):
    cryptogen = SystemRandom()
    for sheet in range(sheets):
        with open("otp" + str(sheet) + ".txt", "w") as f:
            for i in range(length):
                f.write(str(cryptogen.randrange(26)) + "\n") # generates the random number


'''loads a sheet with otp and returns all the numbers in a list'''
def load_sheet(filename):
    with open(filename, "r") as f:
        contents = f.read().splitlines()
    return contents


'''gets the users message in plaintext, returns a lowercase version of it'''
def get_plain_text():
    plain_text = input("Please type your message : ")
    return plain_text.lower()


'''Loads encrypted file'''
def load_file(filename):
    with open(filename, "r") as f:
        contents = f.read()

    return contents


'''Saves encrypted file'''
def save_file(filename, data):
    with open(filename, "w") as f:
        for i in range(0, len(data)-1):
            f.write(str(data.pop(0)) + "\n")



'''Encrypts the plaintext message'''
def encrypt(plaintext, sheet):
    ciphertext = []
    for position, character in enumerate(plaintext):
        if character not in ALPHABET:
            character = ord(character) + int(sheet[position])

            ciphertext.append(character) # if not in alphabet just add that character
        else:
            # int encrypted is the index of that character in the alphabet + the next number in sheet(the otp)
            # mod 26 in case encrypted is greater than 26, so it will always be a valid number
            encrypted = (ALPHABET.index(character) + int(sheet[position])) % 26
            ciphertext.append(ALPHABET[encrypted]) # adds the encrypted character to ciphertext
    return ciphertext


'''Decrypts the encrypted message'''
def decrypt(ciphertext, sheet):
    plaintext = ""
    ciphertext = ciphertext.split("\n")# make ciphertext a list strip out newline
    for position, character in enumerate(ciphertext):
        if character not in ALPHABET:
            character = int(character) - int(sheet[position])
            character = chr(character)
            plaintext += character  # character was never encrypted so just put it back in
        else:
            decrypted = (ALPHABET.index(character) - int(sheet[position])) % 26 # where the decryption happens
            plaintext += ALPHABET[decrypted] # adds decrypted characted to plaintext
    return plaintext



main()