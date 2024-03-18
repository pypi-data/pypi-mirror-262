def RegexSplitter(text, word_regex):
    import re
    return re.findall(word_regex, text)

if __name__ == "__main__":
    word_regex = r'[A-Z][a-z]*'
    text = "ThisIsASamplePythonFile"
    print(RegexSplitter(text, word_regex) == ['This', 'Is', 'A', 'Sample', 'Python', 'File'])
    text = "ThisIsASamplePython"
    print(RegexSplitter(text, word_regex) == ['This', 'Is', 'A', 'Sample', 'Python'])
    text = "ThisIsASamplePythonFile1"
    print(RegexSplitter(text, word_regex) == ['This', 'Is', 'A', 'Sample', 'Python', 'File'])
    text = "ThisIsASampleePython1File1"
    print(RegexSplitter(text, word_regex) == ['This', 'Is', 'A', 'Samplee', 'Python', 'File'])
    word_regex = r'[a-zA-Z]+'
    text = "ThisIsASamplePythonFile"
    print(RegexSplitter(text, word_regex) == ['ThisIsASamplePythonFile'])
    text = "ThisIsASamplePython"
    print(RegexSplitter(text, word_regex) == ['ThisIsASamplePython'])
    text = "ThisIsASamplePythonFile1"
    print(RegexSplitter(text, word_regex) == ['ThisIsASamplePythonFile'])
    text = "ThisIsASampleePython1File1"
    print(RegexSplitter(text, word_regex) == ['ThisIsASampleePython', 'File'])
    word_regex = r'[a-z]+'
    text = "ThisIsASamplePythonFile"
    print(RegexSplitter(text, word_regex) == ['his', 's', 'ample', 'ython', 'ile'])
    text = "ThisIsASamplePython"
    print(RegexSplitter(text, word_regex) == ['his', 's', 'ample', 'ython'])
    text = "ThisIsASamplePythonFile1"
    print(RegexSplitter(text, word_regex) == ['his', 's', 'ample', 'ython', 'ile'])
    text = "ThisIsASampleePython1File1"
    print(RegexSplitter(text, word_regex) == ['his', 's', 'amplee', 'ython', 'ile'])