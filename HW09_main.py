from pathlib import Path


def read_PB(path):  #read phonebook
    dict_ph = {}
    if path.exists():
        with open(path, 'r') as file:        
            for s in file:
                k, v = s.removesuffix('\n').split(':')
                dict_ph[k.strip()] = v.strip()

    return dict_ph


def sort_dict(dict):
    sort_keys = sorted(dict)
    sorted_dict = {i: dict[i] for i in sort_keys}
    return sorted_dict


def write_PB(path, dict_ph):    #write phonebook
    dict_ph = sort_dict(dict_ph)
    list_ph = [f'{k} : {v}' for k,v in dict_ph.items()]
    with open(path, 'w') as file:        
        file.write('\n'.join(list_ph))
    
    return 'Write ok!'


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'bot>> Contact not found'
        except ValueError:
            return 'bot>> Invalid input'
        except IndexError:
            return 'bot>> Invalid data'
    return inner


@input_error
def add_item(name, phone):
    phones_dict[name] = phone
    write_PB(path_file, phones_dict)
    return 'bot>> New item added successfully'


@input_error
def change_phone(name, phone):
    if name in phones_dict:
        phones_dict[name] = phone
        write_PB(path_file, phones_dict)
        return 'bot>> Phone number changed successfully'
    else:
        raise KeyError


@input_error
def get_phone(name):
    if name in phones_dict:
        return 'bot>> ' + phones_dict[name]
    else:
        raise KeyError


@input_error
def show_all():
    if phones_dict:
        list_ph = [f'{k} : {v}' for k,v in phones_dict.items()]         
        return '\n'.join(list_ph)
    

def parser(input_str):
    if input_str.strip().lower() in ["good bye", "close", "exit"]:
        return 'bot>> Good bye!'
    
    elif input_str.strip().lower().startswith('hello'):
        return 'bot>> How can I help you?'
    
    elif 'show all' in input_str.strip().lower():
        return show_all()
    
    elif input_str.strip().lower().startswith('add'):
        data = input_str[3:].strip().split()
        phone = data[-1]
        name = (' ').join(data[:-1])
        return add_item(name, phone)
    
    elif input_str.strip().lower().startswith('change'):
        data = input_str[6:].strip().split()
        phone = data[-1]
        name = (' ').join(data[:-1])
        return change_phone(name, phone)
    
    elif input_str.strip().lower().startswith('phone'):
        name = input_str[5:].strip()
        return get_phone(name)
   
    else:
        return 'bot>> Command was not identified, repeat please'


def main():
    while True:
        input_str = input('bot>> ')
        out_str = parser(input_str)
        print(out_str)
        if out_str == 'bot>> Good bye!':
            break

    
if __name__ == "__main__":
    path_file = Path(__file__).parent / 'phone_book.txt'
    phones_dict = read_PB(path_file)  #phone book -> dict

    main()
