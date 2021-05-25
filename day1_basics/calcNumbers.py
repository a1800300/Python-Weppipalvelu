# This program adds numbers and has conditions

num1 = input('enter first number:')
num2 = input('enter second number:')

sum = num1+num2

if sum == 5:
	print('sum of {0} and {1} is {2} '.format(num1, num2, sum))

else:
	print('sum is not 5')
