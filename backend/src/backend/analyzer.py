import re


units = {
    # ===== SI 기본 단위 (7개) =====
    "kg": {"kg": 1},
    "m": {"m": 1},
    "s": {"s": 1},
    "A": {"A": 1},
    "K": {"K": 1},
    "mol": {"mol": 1},
    "cd": {"cd": 1},

    # ===== SI 유도 단위 (22개) =====

    # 각도
    "rad": {},
    "sr": {},

    # 주파수
    "Hz": {"s": -1},

    # 역학
    "N": {"kg": 1, "m": 1, "s": -2},
    "Pa": {"kg": 1, "m": -1, "s": -2},
    "J": {"kg": 1, "m": 2, "s": -2},
    "W": {"kg": 1, "m": 2, "s": -3},

    # 전자기학
    "C": {"A": 1, "s": 1},
    "V": {"kg": 1, "m": 2, "s": -3, "A": -1},
    "F": {"kg": -1, "m": -2, "s": 4, "A": 2},
    "Ω": {"kg": 1, "m": 2, "s": -3, "A": -2},
    "S": {"kg": -1, "m": -2, "s": 3, "A": 2},
    "Wb": {"kg": 1, "m": 2, "s": -2, "A": -1},
    "T": {"kg": 1, "s": -2, "A": -1},
    "H": {"kg": 1, "m": 2, "s": -2, "A": -2},

    # 온도
    "°C": {"K": 1},

    # 광학
    "lm": {"cd": 1},
    "lx": {"cd": 1, "m": -2},

    # 방사능 / 방사선
    "Bq": {"s": -1},
    "Gy": {"m": 2, "s": -2},
    "Sv": {"m": 2, "s": -2},

    # 촉매 활성
    "kat": {"mol": 1, "s": -1},
}


SUPERSCRIPT = str.maketrans(
    "0123456789-",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
)

def format_result(input):
    result = []

    for key, value in input.items():
        if value != 0:
            result.append(format_unit(key, value))

    return "·".join(result) if result else "1"


def format_unit(unit, exponent):
    if exponent == 0:
        return ""
    if exponent == 1:
        return unit
    return unit + str(exponent).translate(SUPERSCRIPT)

def tokenize(input: str)->list[str]:
    input=input.replace(" ","")
    return re.split(r"([*/^])",input)


def analyze(input:str)-> str:
    """ 
    *, /, ^로 연산되어 있는 단위를 기본 SI unit으로 변환해준다.
    """
    result={}
    tokens=tokenize(input)

    t = tokens[0]
    i=1
    if t in units:
        power=1
        if 2 <len(tokens) and tokens[1]=='^':
            power=int(tokens[2])
            i+=2
        for key, exponent in units[t].items():
            result[key] = result.get(key, 0) + exponent * power
    else:
        raise ValueError(f"잘못된 단위 또는 수식입니다: {t}")
    while i<len(tokens):
        if tokens[i]=='*':
            t=tokens[i+1]
            if t in units:
                power=1
                if i+3<len(tokens) and tokens[i+2]=='^':
                    power=int(tokens[i+3])
                    i+=2                
                for key,exponent in units[t].items():
                    result[key]=result.get(key,0)+exponent*power
                i+=2
            else: raise ValueError(f"잘못된 단위 또는 수식입니다: {t}")
        elif tokens[i]=="/":
            t=tokens[i+1]
            if t in units:
                power=1
                if i+3<len(tokens) and tokens[i+2]=='^':
                    power=int(tokens[i+3])
                    i+=2
                for key,exponent in units[t].items():
                    result[key]=result.get(key,0)-exponent*power
                i+=2
            else: raise ValueError(f"잘못된 단위 또는 수식입니다: {t}")
        else: raise ValueError("잘못된 단위 또는 수식입니다.")
        
    return format_result(result)


if __name__ == "__main__":
    print(tokenize("N*m/s^-2"))
    print(analyze("s/s"))
    print(analyze("N*m"))