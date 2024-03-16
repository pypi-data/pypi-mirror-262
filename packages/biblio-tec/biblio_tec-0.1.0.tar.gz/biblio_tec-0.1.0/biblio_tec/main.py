

class JonaMath:

    def Hello_World():
        print('Hello World!')

    def sum(num1, num2):
        return num1 + num2

    def subtract(num1, num2):
        return num1 - num2

    def multiply(num1, num2):
        return num1 * num2

    def divide(num1, num2):
        # Adiciona uma verificação para evitar divisão por zero
        if num2 == 0:
            return "Erro: Divisão por zero!"
        return num1 / num2

    def exponentiate(base, exponent):
        return base ** exponent