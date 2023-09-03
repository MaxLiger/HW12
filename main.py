from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
import pickle
SAVE_FILE = r"save.bin"

class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    @staticmethod
    def valid_data(value)-> bool:
        if value:
            return True
        return False
    
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, dat):
        if self.valid_data(dat):
            self.__value = dat 


class Name(Field):
    pass


class Phone(Field):
    @staticmethod
    def valid_data(value) -> bool:
        digits = ''.join(filter(str.isdigit, value))
        if 8 < len(digits)<13 and len(value)<20:
            return True
        return False



class Birthday(Field):
    @staticmethod
    def valid_data(value) -> bool:
        if isinstance(value, datetime) and 0 < datetime.now().year - value.year < 100:
            return True
        return False

class Record:
    def __init__(self, name: Name, birthday: Birthday = None, phone: Phone = None) -> None:
        self.name = name
        # self.phones = [phone] if phone else []
        self.birthday = birthday 
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        print(f'Birthday {self.birthday.value} added')


    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            carent_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today >  carent_birthday:
                carent_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (carent_birthday - today).days
        return None


    def add_phone(self, new_phone: str):
        phone = Phone(new_phone)
        self.phones.append(phone)
        print(f'Phone {phone.value} added')


    def delete_phone(self, target_phone: str):
        phone = Phone(target_phone)
        for ph_obj in self.phones:
            if ph_obj.value == phone.value:
                self.phones.remove(ph_obj)
                print(f'Phone {ph_obj.value} removed')


    def change_phone(self, changed_phone: str, phone: str):
        old_phone = Phone(changed_phone)
        new_phone = Phone(phone)
        for ph_obj in self.phones:
            if ph_obj.value == old_phone.value:
                self.phones.remove(ph_obj)
                self.phones.append(new_phone)
                print(f'Phone {ph_obj.value} changed to {new_phone.value}')


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    
    def __iter__(self):
       self.keys_iter = iter(self.data)
       return self
    

    def __next__(self, n=10):
        temp_list=[]
        counter= 0
        try:
            for _ in range(n):
                key = next(self.keys_iter)
                temp_list.append((key, self.data[key]))
        except StopIteration:
            if not temp_list:
               pass # raise StopIteration
        result=''

        for user, user_data in temp_list:
            result += f'\nName: {user}'
            if user_data.birthday:
                result += f', Birthday: {self.data[user].birthday.value.strftime("%d.%m.%Y")}'
            if user_data.phones:
                result += f', Phones:'
                for phone in self.data[user].phones:
                    result += f' {phone.value}'
        return result
    
    
    def save_ab(self, path = SAVE_FILE):
        with open(path, "wb") as file:
            pickle.dump(self.data, file)
    
    
    def load_ab(self, path = SAVE_FILE):
        with open(path, "rb") as file:
            self.data = pickle.load(file)
            
    
    def find(self, key: str)-> list[str]:
        result = ''
        key = key.lower()
        find_users = []
        for user in self.data:
            result += f'{user}'
            # if self.data[user].birthday:
            #     result += f' {self.data[user].birthday.value.strftime("%d.%m.%Y")}'
            if self.data[user].phones:
                for phone in self.data[user].phones:
                    result += f' {phone.value}'
            result +='\n'
        for user in result.split('\n'):
            if key in user.lower():
                find_users.append(user)
        if find_users:
            return find_users
        return 'Not found!'



    
 
   





if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone=phone)
    rec_2 = Record(Name('Bob'))
    rec_3 = Record(Name('Jek'))
    rec.add_phone('0987609893')
    rec_2.add_phone('0987609693')
    rec_3.add_phone('0987608693')
    rec.change_phone('0987609893', '0987609895')
    birth = Birthday(datetime(1991,8,24))
    rec.add_birthday(birth)
    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec_2)
    ab.add_record(rec_3)

    





