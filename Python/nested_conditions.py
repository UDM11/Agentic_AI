user_role = "admin"

is_logged_in = True
if is_logged_in:
    if user_role == "admin":
        print("Wellcome to the admin dashboard and acces granted")
    
    else:
        print("Wellcome to the user dashboard")

else:
    print("Please Log in to the continue")