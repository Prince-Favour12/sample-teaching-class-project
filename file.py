import random as rn
passwords = {
    'User': '12865$553',
    'Excel': '24$#@876',
    'ada': '4509*2#@?1',
    'Prince': 'Prince*$##'
}

# is_upper = False
# is_lower= False
new_password = []
words = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#@$%^&*?")
for user_name, password in passwords.items():
    rn.shuffle(words)
    length = f"{password if (len(password) - 10) > 0 else password + "".join(["".join(rn.choices(words, k= x)) for x in range(1, abs(len(password) - 10)+1)])}"
    if password != length:
        pass
    else:
        print("Updating Users Password...")
        print(f"Do you want to update your password?\nBecause it's not reaching our requirements.")
        user_input = input("Enter Yes or No to continue: ").lower()
        if user_input not in ['yes', 'no']:
            print('invalid')
            break
        elif user_input == 'yes':
            passwords[user_name] = length
        elif user_input == 'no':
            print("Thank you")
            pass

    new_password.append(length)

print(new_password)
# list1 = [1, 2, 3, 4, 5]

# print(rn.choices(list1, k =0))

# print(length)

# for user_name, password in passwords.items():
#     if len(password)>10

