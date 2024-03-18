def encrypt(text):

    def usun_spacje_i_przecinki(text):
        cleaned_text = text.replace(",", "").replace(" ", "")
        return cleaned_text

    def na_binarny(text):
        ascii_values = [ord(char) for char in text]
        binary_values = [format(value, "08b") for value in ascii_values]
        return binary_values

    binary_list = na_binarny(text)

    binary_string = "".join(binary_list)

    cleaned_binary_string = usun_spacje_i_przecinki(binary_string)

    return cleaned_binary_string


def decrypt(dane_binarne):

    def czy_binarna(dane):
        return all(bit == "0" or bit == "1" for bit in dane)

    def binarna_na_tekst(ciag_binarny):
        bajty = [ciag_binarny[i : i + 8] for i in range(0, len(ciag_binarny), 8)]
        liczby_calkowite = [int(bajt, 2) for bajt in bajty]
        tekst = "".join(chr(liczba) for liczba in liczby_calkowite)
        return tekst

    if czy_binarna(dane_binarne):
        dane_tekstowe = binarna_na_tekst(dane_binarne)
    return dane_tekstowe
