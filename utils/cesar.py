def cesar(s: str, k: int) -> str:
    result = []
    for char in s:
        if char.isalpha():
            shift = k % 26
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)

def decesar(s: str, k: int) -> str:
    return cesar(s, -k)

if __name__ == "__main__":
  # Chiffrement
  print(cesar("Hello, World!", 3))        # Khoor, Zruog!
  print(cesar("MNS is great", 2))         # OPU ku itgcv
  print(cesar("Vive le riz crousty", 5))  # Anaj qj wne hwtzxyd

  # Déchiffrement
  print(decesar("Khoor, Zruog!", 3))        # Hello, World!
  print(decesar("OPU ku itgcv", 2))         # MNS is great
  print(decesar("Anaj qj wne hwtzxyd", 5))  # Vive le riz crousty