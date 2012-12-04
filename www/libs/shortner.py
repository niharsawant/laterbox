CHAR_MAP = 'DhQSizIlskKenoErBvRUVugabfMLyHFxwNOYPZGACXpctJTWmjdq5624389170'


def from_decimal(value, base):
  digits = []
  num = value
  output = ''

  while num > 0:
    remainder = num%base
    digits.append(remainder)
    num = num/base
  digits.reverse()

  for x in digits:
    output += CHAR_MAP[x]

  return output

def to_decimal(value, base):
  char_list = list(value)
  char_list.reverse()
  index = output = 0

  for x in char_list:
    output += list(CHAR_MAP).index(x) * pow(base, index)
    index += 1
  return output
