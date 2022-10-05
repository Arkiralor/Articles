from faker import Faker
from secrets import choice
from random import random
import numpy as np

from user_app.models import UserAccount
from user_app.api_helpers import UserAccountHelpers
from scripts import logger


class FakeUser:

    fake = Faker(locale=['en_US', 'en_IN', 'en_UK'])
    dig_list = np.array(tuple((str(i) for i in range(0, 10))))
    token_list = np.array(("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                  "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"))
    alpha_list = np.array(("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                  "r", "s", "t", "u", "v", "w", "x", "y", "z"))
    coin_faces = np.array(("Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails"))

    @classmethod
    def coin_toss(cls, num:int = 100):
        heads = []
        tails = []
        for _ in range(num):
            face = choice(cls.coin_faces)
        
            if face == "Heads":
                heads.append(1)
            elif face == "Tails":
                tails.append(1)
        
        heads = np.array(heads).sum()
        tails = np.array(tails).sum()
        if heads > tails:
            return "Heads"
        elif tails > heads:
            return "Tails"
        else:
            return choice(cls.coin_faces)

    @classmethod
    def create_random_string(cls, size: int = 7):
        char_list = []
        for _ in range(size+1):
            char_list.append(choice(cls.alpha_list))
        return "".join(char_list)

    @classmethod
    def create_user_name(cls):
        username = ""
        user_names = UserAccount.objects.all().values_list("username", flat=True)
        user_names = np.array(user_names)
        while username == "" or username in user_names:
            username = cls.create_random_string(7)

        return username

    @classmethod
    def create_fake_num_stream(cls, max_size: int = 5, min_size: int = 3):
        char_list = []
        for _ in range(random(min_size, max_size)):
            char_list.append(choice(cls.dig_list))

        return ''.join(char_list)

    @classmethod
    def create_fake_phone_number(cls):
        char_list = [
            choice(tuple(str(i) for i in range(6, 10)))
        ]
        for _ in range(9):
            char_list.append(choice(cls.dig_list))        
        return ''.join(char_list)

    @classmethod
    def create_fake_user(cls, num:int=None):
        first_name = cls.fake.first_name()
        last_name = cls.fake.last_name()
        username = cls.create_user_name()

        user_dict = {
            "first_name": first_name,
            "middle_name": cls.fake.first_name() if cls.coin_toss(10) == "Heads" else None,
            "last_name": last_name,
            "username": username,
            "email": f"{username}@gmail.com",
            "mobile": cls.create_fake_phone_number(),
            "password": "Creator@admin1strator!"
        }
        logger.info(f"{num if num else ''}{'. ' if num else ''}Creating fake user: {user_dict.get('email')} .")

        resp = UserAccountHelpers.create_instance(data=user_dict)
        return resp

    @classmethod
    def create_bulk_users(cls, num: int = 55):
        error_list = []
        instance_list = []

        for i in range(1, num+1, 1):
            resp = cls.create_fake_user(num=i)
            if resp.get("error", None):
                logger.warn(resp.get("message"))
                error_list.append(resp.get("message"))
            instance_list.append(resp.get("instance"))

        return instance_list, error_list


def main():
    user_list = FakeUser.create_bulk_users()


if __name__ == "__main__":
    main()
