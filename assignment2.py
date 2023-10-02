eng_alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
eng_alphabet_dict = {letter: index for index, letter in enumerate(eng_alphabet)}
turkish_alphabet = ('A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö', 'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z')
turkish_alphabet_dict = {letter: index for index, letter in enumerate(turkish_alphabet)}
alphabet = eng_alphabet
alphabet_dict = eng_alphabet_dict

def menu():
    while True:
        print("\nSimple Cipher:")
        print("[1] Encrypt")
        print("[2] Decrypt")
        print("[3] Exit")
        print("Selection:")
        selection = input()
        if len(selection) > 0:
            if(selection == "tr"):
                return '81'
            first_letter = selection[0].lower()
            if first_letter in ["1", "2", "3"]:
                return first_letter
        print("Invalid selection. Please try again.")

def adjustString(s):
    only_alpha = ''.join(c for c in s if c.isalpha())
    upper_cased = only_alpha.upper()
    return upper_cased


def getStringWithMessage(message):
    while True:
        print(message)
        plainText = input()
        adjustedString = adjustString(plainText)
        if len(adjustedString) > 0:
            return adjustedString
        else:
            print("Entered string must at least have 1 alpahabet character.")
        
def inputPlainText():
    return getStringWithMessage("Enter the plaintext message:")

def inputCipherText():
    return getStringWithMessage("Enter the ciphertext message:")

def inputKey():
    return deleteRepeatingCharInKey(getStringWithMessage("Enter the key:"))

def deleteRepeatingCharInKey(key):
    pureKey = ""
    uniqueChars = set(key)
    for chr in key:
        if chr not in pureKey:
            pureKey += chr
    return pureKey

def adjustKey(key, plainText):
    adjustedKey = ""
    length = len(plainText)
    for i in range(length):
        adjustedKey += key[i % len(key)]
    return adjustedKey           

def vigenereEncrypt(plainText, adjustedKey):
    cipherText = ""
    #operations
    for i in range(len(plainText)):
        index1 = alphabet_dict[adjustedKey[i]] 
        index2 = alphabet_dict[plainText[i]]
        index3 = (index1 + index2) % len(alphabet)
        cipherText += alphabet[index3]
    return cipherText

def vigenereDecrypt(cipherText, adjustedKey):
    plainText = ""
    aysem = len(cipherText)
    for i in range(len(cipherText)):
        index1 = alphabet_dict[adjustedKey[i]]
        index2 = alphabet_dict[cipherText[i]]
        index3 = (index2 - index1) % len(alphabet)
        plainText += alphabet[index3]
    return plainText

def divedeStringToSubstrings(text, key):
    subStrings = []
    for i in range(len(key)):
        subString = key[i]
        subStrings.append(subString)
    for i in range(len(text)):
        subStrings[i%len(key)] += text[i]
    return subStrings

def reverseDivideStringToSubstrings(text,key): #lata asfasdfasdfasdfasd;fljasdjhfdkjashfasjdf
    subStrings = []
    columnCount = len(key)
    rowCount = len(text) // len(key)
    for i in range(columnCount):
        subString = ""
        for j in range(rowCount):
            index = (j*columnCount)+i
            subString += text[index]
        subStrings.append(subString)
    return subStrings


def divideStringAndAddPadding(plainText,key):
    subStrings = divedeStringToSubstrings(plainText,key)    

    for i in range(1,len(subStrings)): #first one cannot be missing
        if len(subStrings[i]) < len(subStrings[0]):
            missingCharCount = len(subStrings[0]) - len(subStrings[i])
            subStrings[i] += 'Z' * missingCharCount #Z is the least used char in english

    return subStrings


def orderSubstringsAndRemoveFirstLetter(subStrings):
    sortedList = sorted(subStrings)
    removedFirstLetterList = [s[1:] for s in sortedList]
    return removedFirstLetterList

def takeToOriginalOrder(subStrings,key):
    originalOrder = []
    for letter in key:
        for i in range(len(subStrings)):
            if letter == subStrings[i][0]:
                originalOrder.append(subStrings[i][1:])
                subStrings.pop(i)
                break
    return originalOrder

def getPlaintextOfTransposed(originalOrderSubStrings,key):
    rowCount = len(originalOrderSubStrings[0])
    plainText = ""
    for i in range(rowCount):
        for j in range(len(key)):
            plainText += originalOrderSubStrings[j][i]

    return plainText
    
def columnarEncrypt(plainText, key):
    subStrings = divideStringAndAddPadding(plainText, key)
    sortedStrings = orderSubstringsAndRemoveFirstLetter(subStrings)
    output = ""
    for string in sortedStrings:
        output += string
    return output

def columnarDecrypt(cipherText, key):
    orderedKey = "".join(sorted(key))
    substrings = []
    rowCount = len(cipherText) // len(key)
    for i in range(len(key)):
        substring = orderedKey[i]
        for j in range((i*rowCount),(i*rowCount + rowCount)):
            substring += cipherText[j]
        substrings.append(substring)

    originalOrdered = takeToOriginalOrder(substrings,key)
    decryptedColumnarText = getPlaintextOfTransposed(originalOrdered,key)
    return decryptedColumnarText
    
def encryption():
    plainText = inputPlainText()
    key = inputKey()
    keyWithSameLength = adjustKey(key,plainText) #key and plain text should have same amount of chars(modulation also could be used)
    print("************************Encryption************************")
    print("\tPhase: Vigenere Cipher")
    print("\t>> Input:",plainText)
    print("\t>> Key:",key)
    vigenereEncrypted = vigenereEncrypt(plainText,keyWithSameLength)
    print("\t>> Output:", vigenereEncrypted)
    
    print()

    print("\tPhase: Columnar Transposition Cipher")
    print("\t>> Input: ",vigenereEncrypted)
    print("\t>> Key: ", key)
    columnarEncrypted = columnarEncrypt(vigenereEncrypted,key)
    print("\t>> Output: ",columnarEncrypted)
    print("**********************************************************")


def decryption():
    cipherText = inputCipherText()
    key = inputKey()
    print("************************Decryption************************")
    print("\tPhase: Columnar Transposition Cipher")
    print("\t>> Input:",cipherText)
    print("\t>> Key:",key)
    adjustedKey = adjustKey(key,cipherText)
    decrypedColumnarText =columnarDecrypt(cipherText,key)
    print("\t>> Output:", decrypedColumnarText)
    plainText = vigenereDecrypt(decrypedColumnarText,adjustedKey)
    print("\tPhase: Vigenere Cipher")
    print("\t>> Input:",decrypedColumnarText)
    print("\t>> Key:",key)
    print("\t>> Output: ",plainText)
    print("**********************************************************")

def toggleLanguage(turkishMode):
    turkishMode = not turkishMode
    global alphabet
    global alphabet_dict
    if(turkishMode):
        print("Secret Turkish Mode Activated!")
        alphabet = turkish_alphabet
        alphabet_dict = turkish_alphabet_dict
    else:
        print("Secret Turkish Mode Deactivated!")
        alphabet = eng_alphabet
        alphabet_dict = eng_alphabet_dict
    return turkishMode
        

#nalcxehwttdttfseeleedsoaxfeahl
def main():
    turkishMode = False
    menuChoice = '0'

    while menuChoice != '3':
        menuChoice = menu()
        if menuChoice == '1':
            encryption()
        elif menuChoice == '2':
            decryption()
        elif menuChoice == '81':
            turkishMode = toggleLanguage(turkishMode)
        else:
            print("Bye!")
main()
