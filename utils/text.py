def separate_paragraph(text, max_words, max_word_size):
  words = text.split(' ')
  new_text = ''
  count = 0
  for word in words:
    if len(word) > max_word_size:
      new_text += '\n' + word + ' '
      count += 2
    elif count < max_words:
      new_text += word + ' '
      count += 1
    else:
      new_text += '\n' + word + ' '
      count = 1
  return new_text
