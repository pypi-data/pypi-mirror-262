import random
from typing import Final
import json

class ReviewParser:
  # Maximum tries for user to answer
  MAX_TRIES: Final = 3

  # Valid options
  VALID_OPTIONS: Final[list[str]] = [
    'enumeration',
    'identification',
    'multiple_choice',
  ]

  # Valid question types
  VALID_Q_TYPES: Final[list[str]] = [
    'enums',
    'qa',
    'choices'
  ]

  def __init__(
      self, 
      questions: list[dict[str, str]] = None, 
      enums: list[dict[str, str]] = None,
      options: dict[str, str] = None,
      sequence: list[str] = None
    ) -> None:

    # Set score and total questions to 0
    self.score = 0
    self.total = 0

    self.questions: list[dict[str, str]] = questions or []
    self.enums: list[dict[str, str]] = enums or []

    self._questions = []
    self._enums = []

    # Verify options
    if options:
      for key in options.keys():
        assert key.strip().lower() in ReviewParser.VALID_OPTIONS, f"Option {key} is not existing in this context."

    else:
      options = {
        'enumeration': True,
        'identification': True,
        'multiple_choice': True,
      }

    self._options = options

    # Verify sequence
    if sequence:
      for s in sequence:
        assert s.strip().lower() in ReviewParser.VALID_Q_TYPES, f"Question type in your sequence does not exist in this context."

      self._sequence = sequence

    else:
      self._sequence = None

  def addQuestionSet(self, question_set: dict[str, str]) -> None:
    self.questions.append(question_set)

  def addEnumsSet(self, enum_set: dict[str, str]) -> None:
    self.enums.append(enum_set)

  def _parseReferences(self) -> None:
    for q in self.questions:
      keys = list(q.keys())
      random.shuffle(keys)

      self._questions.extend([(key, q[key]) for key in keys])

    for e in self.enums:
      keys = list(e.keys())
      random.shuffle(keys)

      self._enums.extend([(key, e[key]) for key in keys])

  def _resetToInitialState(self) -> None:
    self.score = 0
    self.total = 0
    self._parseReferences()

  def _initializeOptions(self, options=None) -> None:
    # Initialize options
    if options:
      # Verify options
      for key in options.keys():
        assert key in ReviewParser.VALID_OPTIONS, f"Option {key} is not existing in this context."

      enumeration = options.get('enumeration', False)
      identification = options.get('identification', False)
      multiple_choice = options.get('multiple_choice', False)
    else:
      enumeration = self._options.get('enumeration', False)
      identification = self._options.get('identification', False)
      multiple_choice = self._options.get('multiple_choice', False)

    return enumeration, identification, multiple_choice

  def start(self, options: dict[str, any] | None = None, sequence: list[str] | None = None) -> None:

    # Initialize options
    enumeration, identification, multiple_choice = self._initializeOptions(options)

    # Initialize sequence
    if sequence:
      for s in sequence:
        assert s.strip().lower() in ReviewParser.VALID_Q_TYPES, f"Question type in your sequence does not exist in this context."

    else:
      sequence = self._sequence

    # Return if all parameters are false
    if not (
      enumeration or
      identification or
      multiple_choice
    ):
      self._end()
      return
    
    # Reset to initial state
    self._resetToInitialState()

    # Create a deepcopy of questions and enums
    questions = [*self._questions]
    enums = [*self._enums]

    # Flag to track if question pool is empty
    empty = 0

    while empty != 2 and sequence:
      if not sequence:
        # Toss coin to pick whether to choose question from enums or QA
        modes = ['Enums', 'QA', 'Choices']

        if not enums or not enumeration:
          modes.remove('Enums')
        if not identification or not questions:
          modes.remove('QA')
        if not multiple_choice or (not questions and not enums):
          modes.remove('Choices')

        toss_coin = random.choice(modes)

      else:
        toss_coin = sequence[0]

      curr_tries = ReviewParser.MAX_TRIES

      match toss_coin.lower():
        case 'qa':
          # Base-case
          if not questions:
            empty += 1
            self._sequence.remove('qa')
            continue

          # Increment total question counter
          self.total += 1

          # Obtain random question
          random_qa = random.choice(questions)
          questions.remove(random_qa)

          answer, question = random_qa

          # Questions are list of different questions associated to the same answer
          print(f'Question: {random.choice(question)}')

          while curr_tries > 0:

            # Wait for user input
            useranswer = input('Answer: ')

            # Cleanse user answer and correct answer
            # Correct answer is a string delimited by a pipe character for acceptable answers
            answers = answer.split('|')
            answers = [a.strip() for a in answers] # Do not apply lower-case here for print purposes

            # Compare user answer to acceptable answers
            if any(useranswer.strip().lower() == a.lower() for a in answers):
              self.score += 1 * curr_tries # Scoring system
              print('\n** Correct **\n')
              break

            print('\n** Incorrect **\n')

            curr_tries -= 1
          else:
            print(f'Correct answers are: ', end='')
            print(*answers, sep=', ', end='\n\n')

        case 'enums':
          # Base-case
          if not enums:
            empty += 1
            self._sequence.remove('enums')
            continue

          # Get a random question and remove it from the pool
          random_enums = random.choice(enums)
          enums.remove(random_enums)

          question, answers = random_enums
          total_answers = len(answers)

          # Increment question counter
          self.total += total_answers

          print(f'Enumerate: {question}')

          # Correct answers are identification enumerations
          # Each correct answers are delimited by a pipe character for acceptable answers
          # Loop for user input up to the number of correct answers
          useranswers: list[str] = []

          for _ in range(len(answers)):
            useranswers.append(input(f'Answer #{_ + 1}: '))

          # Number of correctly answered instances
          correct = 0

          # Store index of checked answers to avoid duplication of correct instances
          checked = []

          # Store correctly answered enums
          right_answers = []

          # Validate answers
          for ans in useranswers:
            for idx, correct_ans in enumerate(answers):
              # Check if current index is present in the checked answers
              if idx in checked:
                continue

              # Parse and cleanse correct answers
              correct_ans = correct_ans.split('|')
              correct_ans = [c.strip() for c in correct_ans] # Do not apply lower-case here for print purposes

              # Checking
              for c in correct_ans:
                if ans.strip().lower() == c.lower():
                  correct += 1
                  right_answers.append(c)
                  checked.append(idx)
                  break

          # Micro assessment
          if correct == len(answers):
            self.score += correct * ReviewParser.MAX_TRIES
            print("\n** Correct **\n")

          else:
            print(f'\nCorrect answers are: ', end='')
            print(*answers, sep=', ', end='\n')
            print(f'Your correct answers: ', end='')
            print(*right_answers, sep=', ', end='\n\n')
    
        case 'choices':
          # Base-case
          if not questions and not enums:
            empty = 2
            self._sequence.remove('choices')

          # Obtain either a random question or enumeration
          random_q = random.choice(questions + enums)

          # Determine if chosen is from questions or enums list
          q_type = 1 if random_q in questions or not enums else \
                   0 if random_q in enums or not questions else -1

          # Separate logic for each question type
          match q_type:
            case 0:
              # Enums type
              # Increment total question count
              self.total += 1

              # Remove question from enums array
              enums.remove(random_q)

              # Extract the question and answer
              question, answers = random_q

              # Answers are list of enumerations, choose 1 
              answer = random.choice(answers)
              answer = answer.split("|")[0].strip()

              # Obtain choices from different existing questions
              choices = []
              while len(choices) < 3:
                for a in random.sample(self._questions + self._enums, 3):
                  if a[0] == question:
                    continue

                  if a in self._enums:
                    c = random.choice(a[1])
                    c = c.split("|")[0].strip()

                  else:
                    c = a[0].split("|")[0].strip()
                  
                  if (c != answer and 
                      c not in choices and
                      a[0] not in self._enums[self._enums.index((question, answers))][1]
                    ):
                    choices.append(c)
                    if len(choices) == 3:
                      break

              choices.append(answer)
              random.shuffle(choices)

              # Print question
              print(f'Multiple Choice: It is under "{question}".')

              # Print the choices
              for idx, c in enumerate(choices):
                print(f'{chr(ord('a') + idx)}. {c}')

              while curr_tries > 0:

                # Wait for user input
                useranswer = input('Answer: ')

                if useranswer == '':
                  curr_tries -= 1
                  continue

                # Answer taken will be the first character only, regardless of input
                useranswer = useranswer.strip().lower()[0]

                # Verify answer
                if useranswer == chr(ord('a') + choices.index(answer)).lower() or \
                   useranswer == str(choices.index(answer) + 1):
                  self.score += 1 * curr_tries # Scoring system
                  print('\n** Correct **\n')
                  break

                print('\n** Incorrect **\n')

                curr_tries -= 1

              else:
                print(f"Correct answer is letter {chr(ord('a') + choices.index(answer)).upper()}")

            case 1:
              # Identification type
              # Increment total question count
              self.total += 1

              # Remove question from questions array
              questions.remove(random_q)

              # Extract the question and answer
              answer, question = random_q
              answer = answer.split("|")[0].strip()

              # Obtain choices from different existing questions
              choices = []
              while len(choices) < 3:
                for a in random.sample(self._questions + self._enums, 3):
                  if a in self._enums:
                    c = random.choice(a[1])
                    c = c.split("|")[0].strip()

                  else:
                    c = a[0].split("|")[0].strip()

                  if c != answer or c not in choices:
                    choices.append(c)
                    if len(choices) == 3:
                      break

              choices.append(answer)
              random.shuffle(choices)

              # Questions are list of different questions associated to the same answer
              print(f'Multiple Choice: {random.choice(question)}')

              # Print the choices
              for idx, c in enumerate(choices):
                print(f'{chr(ord('a') + idx)}. {c}')

              while curr_tries > 0:

                # Wait for user input
                useranswer = input('Answer: ')

                # Answer taken will be the first character only, regardless of input
                if useranswer == '':
                  curr_tries -= 1
                  continue

                useranswer = useranswer.strip().lower()[0]

                # Verify answer
                if useranswer == chr(ord('a') + choices.index(answer)).lower() or \
                   useranswer == str(choices.index(answer) + 1):
                  self.score += 1 * curr_tries # Scoring system
                  print('\n** Correct **\n')
                  break

                print('\n** Incorrect **\n')

                curr_tries -= 1

              else:
                print(f"Correct answer is letter {chr(ord('a') + choices.index(answer)).upper()}")
                  

    # Clean-up
    self._end()

  def _end(self) -> None:
    print(f'Your score is: {self.score}')
    print(f'Total score is: {self.total * ReviewParser.MAX_TRIES}')

  def LoadNotesFromJson(json_path) -> dict[str, str]:
    with open(json_path) as file:
      return json.load(file)