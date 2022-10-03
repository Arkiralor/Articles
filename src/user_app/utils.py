from secrets import token_hex, choice


class UserOTPUtils:

    digit_seq = tuple((i for i in range(0, 10)))
    letter_seq = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
    spec_seq = ("!", "@", "#", "$", "%", "^", "&")
    hex_digits = ("0", "1", "2", "3", "4", "5", "6", "7", "8",
                  "9", "10", "a", "b", "c", "d", "e", "f")

    @classmethod
    def create_mixed_otp(cls, size: int = 6):
        otp_list = []

        for _ in range(size+1):
            otp_list.append(
                str(
                    choice(
                        cls.digit_seq
                        + cls.letter_seq
                        + cls.spec_seq
                    )
                )
            )

        otp = ''.join(otp_list)
        return otp

    @classmethod
    def create_alphanumeric_otp(cls, size: int = 6):
        otp_list = []

        for _ in range(size+1):
            otp_list.append(
                str(
                    choice(
                        cls.digit_seq
                        + cls.letter_seq
                    )
                )
            )

        otp = ''.join(otp_list)
        return otp

    @classmethod
    def create_alphabet_otp(cls, size: int = 6):
        otp_list = []

        for _ in range(size+1):
            otp_list.append(
                str(
                    choice(
                        cls.letter_seq
                    )
                )
            )

        otp = ''.join(otp_list)
        return otp

    @classmethod
    def create_numeric_otp(cls, size: int = 6):
        otp_list = []

        for _ in range(size+1):
            otp_list.append(
                str(
                    choice(
                        cls.digit_seq
                    )
                )
            )

        otp = ''.join(otp_list)
        return otp

    @classmethod
    def create_hex_otp(cls, size: int = 6):
        otp_list = []

        for _ in range(size+1):
            otp_list.append(
                str(
                    choice(cls.hex_digits)
                )
            )

        otp = ''.join(otp_list)
        return otp
