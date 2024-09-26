import upytest

 # cases = ["sum(11, 0)", "sum(10, 0)"]
def sum(a, b):
    if a + b > 10:
        print("Yes")
    else:
        print("No")

upytest.utest(__file__, sum)