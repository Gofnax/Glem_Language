from functools import reduce
from itertools import accumulate

# Question 1
generate_first_n_fibonacci_numbers = lambda n : [0] if n == 0 else [0, 1] if n == 1 else (lambda sequence : sequence + [sequence[-1] + sequence[-2]])(generate_first_n_fibonacci_numbers(n - 1))


# Question 2
# Note: Since the behavior in that case was not clearly defined, the answer below does not handle empty lists.
concatenate_strings = lambda strings : strings[0] if len(strings) == 1 else strings[0] + ' ' + concatenate_strings(strings[1:])


# Question 3
accumulate_squares_of_even_numbers = lambda number_lists : list(accumulate((lambda number_lists : [squared_even_number for squared_even_numbers in [(lambda numbers : map(lambda number : number ** 2, filter(lambda number : number % 2 == 0, numbers)))(numbers) for numbers in number_lists] for squared_even_number in squared_even_numbers])(number_lists)))


# Question 4
# Note: The answer below was made under the assumption that applying the operation cumulatively would produce a sequence, similar to how cumulative summation works.
def make_cumulative(binary_operation):
  return lambda sequence : list(accumulate(sequence, binary_operation))

factorial = lambda n : 1 if n == 0 else make_cumulative(lambda x, y : x * y)(range(1, n + 1))[-1]

exponentiation = lambda base, power : make_cumulative(lambda x, y : x * y)([base] * power)[-1]


# Question 5
print((lambda numbers : reduce(lambda accumulator, current_number : accumulator + current_number, list(map(lambda number : number ** 2, filter(lambda number : number % 2 == 0, numbers))), 0))([1, 2, 3, 4, 5, 6]))


# Question 6
count_palindromes = lambda string_lists : list(map(lambda strings : len(list(filter(lambda string : string == string[::-1], map(lambda string : string.lower().replace(' ', ''), strings)))), string_lists))


# Question 7 – Lazy evaluation refers to the concept of deferring the computation of some value until that value is actually required for some action, rather than computing it in advance.
# In the context of the provided program, we have generate_values return a generator iterator, which computes the next value in a sequence only when called on (via next()). In the first section, we see that generate_values() is converted to a list, meaning it is iterated through and its values are computed and then stored in the resulting list. Only after all the elements had been computed is the list iterated through and the square function is applied to them.
# In the subsequent section, instead of iterating through the list, we iterate through the generator iterator, which means that in every iteration, the current value is computed just as it is passed to the square function, meaning it is evaluated lazily.


# Question 8
get_primes_reversed = lambda numbers : sorted([number for number in numbers if reduce(lambda is_prime, divisor : is_prime and number % divisor != 0, range(2, int(number ** 0.5) + 1), True)], key=None, reverse=True)