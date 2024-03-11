def rtrim(s, t=" \t\n\r\f\v"):
    return s[:s.rfind(t) + 1] if t in s else s

def ltrim(s, t=" \t\n\r\f\v"):
    return s[s.find(t) + 1:] if t in s else s

def trim(s, t=" \t\n\r\f\v"):
    return ltrim(rtrim(s, t), t)

def tokenizer(line, delimeter):
    return [trim(word) for word in line.split(delimeter)]

MAX_LINES = 1000

def read_text_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

if __name__ == "__main__":
    # tokens = tokenizer("add r1, r2, r3", ' ')
    # for token in tokens:
    #     if token:
    #         print(token)
        
    filename = "src/instruction/text.txt"
    lines = read_text_file(filename)
    tokens = tokenizer(lines[0], ' ')
    for token in tokens:
        sub_tokens = tokenizer(token, ',')
        for sub_token in sub_tokens:
            if sub_token:
                print(sub_token)
